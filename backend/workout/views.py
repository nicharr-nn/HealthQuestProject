from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import WorkoutProgramSerializer
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .xp_rules import calculate_xp
from django.apps import apps
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .models import WorkoutProgram, WorkoutAssignment, WorkoutDayCompletion
from django.utils import timezone
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
import calendar

User = get_user_model()

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def workout_programs(request):
    """
    GET: List all workout programs
    POST: Create a new workout program (coaches only)
    """
    if request.method == 'GET':
        queryset = WorkoutProgram.objects.all()
        serializer = WorkoutProgramSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        profile = request.user.userprofile
        if profile.role != "coach":
            raise PermissionDenied("Only coaches can create programs")

        serializer = WorkoutProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(coach=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def workout_assignments(request, id):
    """Assign a workout program to a member (coaches only)"""
    coach_profile = request.user.userprofile
    if coach_profile.role != "coach":
        raise PermissionDenied("Only coaches can assign programs")

    member = get_object_or_404(User, pk=id).userprofile
    program_id = request.data.get("program_id")
    program = get_object_or_404(WorkoutProgram, pk=program_id)

    assignment = WorkoutAssignment.objects.create(
        user_profile=member, program=program
    )
    return Response({"message": "Program assigned", "assignment_id": assignment.id})

@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def workout_assignments_update(request, id):
    """Complete or delete a workout assignment (members only)"""
    profile = request.user.userprofile
    assignment = get_object_or_404(WorkoutAssignment, pk=id, user_profile=profile)

    if profile.role != "member":
        raise PermissionDenied("Only members can complete/delete assignments")

    if request.method == "PATCH":
        difficulty = assignment.program.difficulty_level
        duration = assignment.program.duration
        xp = calculate_xp(duration=duration, difficulty_level=difficulty)

        assignment.status = "completed"
        assignment.completed_date = timezone.now()
        assignment.save()

        # Log completion
        WorkoutDayCompletion.objects.create(
            assignment=assignment, user_profile=profile, xp_earned=xp
        )

        # Update user XP
        ul = profile.get_current_level()
        ul.add_xp(xp)

        return Response({"message": "Assignment completed", "xp_awarded": xp})

    elif request.method == "DELETE":
        assignment.delete()
        return Response({"message": "Assignment deleted"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def todays_workout(request):
    profile = request.user.userprofile
    # choose the next active assignment for the user
    assignment = WorkoutAssignment.objects.filter(user_profile=profile, status='assigned').order_by('created_at').first()
    if not assignment:
        return Response({"message": "No active assignment"}, status=200)
    program = assignment.program
    # return basic program + assignment id
    return Response({
        "assignment_id": assignment.id,
        "program": {
            "id": program.id,
            "name": program.name,
            "description": program.description,
            "duration": program.duration,
            "difficulty_level": program.difficulty_level,
            "xp": program.xp if hasattr(program, 'xp') else None
        }
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_analytics(request):
    profile = request.user.userprofile
    today = timezone.localdate()

    # --- Weekly windows ---
    week_start = today - timedelta(days=6)
    prev_week_start = week_start - timedelta(days=7)
    prev_week_end = week_start - timedelta(days=1)

    this_week_count = WorkoutDayCompletion.objects.filter(
        user_profile=profile,
        completed_at__date__gte=week_start
    ).count()

    prev_week_count = WorkoutDayCompletion.objects.filter(
        user_profile=profile,
        completed_at__date__range=(prev_week_start, prev_week_end)
    ).count()

    if prev_week_count == 0:
        weekly_improvement = 100 if this_week_count > 0 else 0
    else:
        weekly_improvement = round(((this_week_count - prev_week_count) / prev_week_count) * 100, 1)

    # --- Consistency (last 30 days) ---
    month_start = today - timedelta(days=29)
    days_with_activity = WorkoutDayCompletion.objects.filter(
        user_profile=profile,
        completed_at__date__gte=month_start
    ).values("completed_at__date").distinct().count()

    consistency = round((days_with_activity / 30) * 100, 1)

    # --- XP last 30 days ---
    xp_agg = WorkoutDayCompletion.objects.filter(
        user_profile=profile,
        completed_at__date__gte=month_start
    ).aggregate(total_xp=Sum("xp_earned")) or {}

    xp_last_30 = xp_agg.get("total_xp") or 0

    # --- Monthly challenge ---
    target = getattr(profile, "monthly_challenge_target", 20)
    completed_month = WorkoutDayCompletion.objects.filter(
        user_profile=profile,
        completed_at__date__gte=today.replace(day=1)
    ).count()

    _, days_in_month = calendar.monthrange(today.year, today.month)
    last_day_of_month = today.replace(day=days_in_month)
    days_left = (last_day_of_month - today).days

    # --- Current streak calculation ---
    completions = WorkoutDayCompletion.objects.filter(
        user_profile=profile
    ).values_list("completed_at__date", flat=True).distinct().order_by("-completed_at__date")

    streak = 0
    if completions:
        current_day = today
        for workout_date in completions:
            if workout_date == current_day:
                streak += 1
                current_day -= timedelta(days=1)
            else:
                break

    payload = {
        "analytics": {
            "weeklyImprovement": weekly_improvement,
            "consistency": consistency,
            "xp_last_30_days": xp_last_30,
            "completed_this_week": this_week_count,
            "completed_prev_week": prev_week_count,
            "current_streak": streak,  # 🔥 New field
        },
        "monthlyChallenge": {
            "description": f"Complete {target} workouts this month",
            "completed": completed_month,
            "target": target,
            "daysLeft": days_left,
        }
    }
    return Response(payload)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_weekly_activity(request):
    """
    Return last 7 days of activity for the authenticated user.
    Response: [{ label, date, count, height, isActive }, ...] (7 items, oldest -> newest)
    height is a normalized integer 20-100 for frontend bar rendering.
    """
    user_profile = request.user.userprofile
    today = timezone.localdate()
    days = []
    counts = []

    # collect counts per day (oldest -> newest)
    for days_ago in range(6, -1, -1):
        d = today - timedelta(days=days_ago)
        cnt = WorkoutDayCompletion.objects.filter(
            user_profile=user_profile,
            completed_at__date=d
        ).count()
        counts.append({"date": d, "count": cnt})

    # compute normalization (avoid zero division)
    max_count = max(item["count"] for item in counts) or 0

    result = []
    for item in counts:
        d = item["date"]
        cnt = item["count"]
        # normalize height to 20..100 so very small values are visible
        if max_count > 0:
            height = int(20 + (cnt / max_count) * 80)
        else:
            height = 20 if cnt == 0 else 100
        result.append({
            "label": d.strftime("%a")[0],         # 'M','T','W','T','F','S','S'
            "date": d.isoformat(),
            "count": cnt,
            "height": height,                   # for bar height in UI
            "isActive": cnt > 0
        })

    return Response(result)
