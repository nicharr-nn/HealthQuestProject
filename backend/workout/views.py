import calendar
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    WorkoutDay,
    WorkoutDayCompletion,
    WorkoutProgram,
    WorkoutAssignment,
)
from .serializers import WorkoutProgramSerializer, WorkoutAssignmentSerializer
from .xp_rules import calculate_xp, COMPLETION_BONUS


User = get_user_model()


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def workout_programs(request):
    if request.method == "GET":
        user_profile = request.user.userprofile
        user_level = user_profile.get_current_level()

        # Build query based on user's level
        level_filters = models.Q(level_access="all")
        if user_level.level_rank >= 1:  # Bronze and above
            level_filters |= models.Q(level_access="bronze")
        if user_level.level_rank >= 2:  # Silver and above
            level_filters |= models.Q(level_access="silver")
        if user_level.level_rank >= 3:  # Gold and above
            level_filters |= models.Q(level_access="gold")

        # Role-based filtering
        if user_profile.role == "coach":
            programs = WorkoutProgram.objects.filter(
                models.Q(coach=user_profile)
                | (models.Q(is_public=True) & level_filters)
            ).distinct()

        elif user_profile.role == "member":
            # Members see: public programs matching their level + assigned programs
            member_obj = getattr(user_profile, "member_profile", None)

            if member_obj:
                # Get assigned program IDs
                assigned_program_ids = WorkoutAssignment.objects.filter(
                    member=member_obj
                ).values_list("program_id", flat=True)

                programs = WorkoutProgram.objects.filter(
                    (models.Q(is_public=True) & level_filters)
                    | models.Q(id__in=assigned_program_ids)
                ).distinct()
            else:
                # No member profile, only show public programs by level
                programs = (
                    WorkoutProgram.objects.filter(is_public=True)
                    .filter(level_filters)
                    .distinct()
                )

        else:  # Normal users
            programs = (
                WorkoutProgram.objects.filter(is_public=True)
                .filter(level_filters)
                .distinct()
            )

        serializer = WorkoutProgramSerializer(programs, many=True)
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_workout_programs(request):
    if request.method == "POST":
        user_profile = request.user.userprofile

        if user_profile.role != "coach":
            return Response(
                {"error": "Only coaches can create workout programs"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Create program with serializer
        data = request.data.copy()

        # Ensure coach is set to current user
        data["coach"] = user_profile.id

        serializer = WorkoutProgramSerializer(data=data)
        if serializer.is_valid():
            program = serializer.save()

            # Return the created program
            response_serializer = WorkoutProgramSerializer(program)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def workout_program_detail(request, id):
    """
    GET: Retrieve a specific workout program
    PUT/PATCH: Update a workout program
    DELETE: Delete a workout program
    """
    program = get_object_or_404(WorkoutProgram, pk=id)

    if request.method == "GET":
        serializer = WorkoutProgramSerializer(program)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_workout_program(request, id):
    program = get_object_or_404(WorkoutProgram, pk=id)
    user_profile = request.user.userprofile

    if request.method in ["PUT", "PATCH"]:
        # Only the coach who created it can update
        if program.coach != user_profile:
            return Response(
                {"error": "You don't have permission to update this program"},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data.copy()
        days_data = data.pop("days", None)

        # Update program fields
        serializer = WorkoutProgramSerializer(
            program, data=data, partial=(request.method == "PATCH")
        )

        if serializer.is_valid():
            updated_program = serializer.save()

            if days_data is not None:
                # Delete existing days
                WorkoutDay.objects.filter(program=updated_program).delete()

                # Create new days
                for day_data in days_data:
                    duration_value = day_data.get("duration")

                    WorkoutDay.objects.create(
                        program=updated_program,
                        day_number=day_data.get("day_number"),
                        title=day_data.get(
                            "title", f"Day {day_data.get('day_number')}"
                        ),
                        type=day_data.get("type", ""),
                        video_links=day_data.get("video_links", []),
                        duration=duration_value,
                    )

            # Return updated program with days
            response_serializer = WorkoutProgramSerializer(updated_program)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_workout_program(request, id):
    program = get_object_or_404(WorkoutProgram, pk=id)
    user_profile = request.user.userprofile
    if request.method == "DELETE":
        # Only the coach who created it can delete
        if program.coach != user_profile:
            return Response(
                {"error": "You don't have permission to delete this program"},
                status=status.HTTP_403_FORBIDDEN,
            )

        program.delete()
        return Response(
            {"message": "Program deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_analytics(request):
    """Return user workout analytics."""
    profile = request.user.userprofile
    today = timezone.localdate()

    # Get base queryset
    completions = WorkoutDayCompletion.objects.filter(user_profile=profile)

    # Calculate all metrics
    weekly_stats = _calculate_weekly_improvement(completions, today)
    consistency_stats = _calculate_consistency(completions, today)
    xp_stats = _calculate_xp_last_30_days(completions, today)
    monthly_stats = _calculate_monthly_challenge(completions, profile, today)
    streak = _calculate_current_streak(completions, today)

    return Response(
        {
            "analytics": {
                "weeklyImprovement": weekly_stats["improvement"],
                "consistency": consistency_stats["percentage"],
                "xp_last_30_days": xp_stats["total"],
                "completed_this_week": weekly_stats["this_week"],
                "completed_prev_week": weekly_stats["prev_week"],
                "current_streak": streak,
            },
            "monthlyChallenge": monthly_stats,
        }
    )


def _calculate_weekly_improvement(completions, today):
    """Calculate weekly workout improvement percentage."""
    week_start = today - timedelta(days=6)
    prev_week_start = week_start - timedelta(days=7)
    prev_week_end = week_start - timedelta(days=1)

    this_week = completions.filter(completed_at__date__gte=week_start).count()
    prev_week = completions.filter(
        completed_at__date__range=(prev_week_start, prev_week_end)
    ).count()

    if prev_week == 0:
        improvement = 100 if this_week > 0 else 0
    else:
        improvement = round(((this_week - prev_week) / prev_week) * 100, 1)

    return {
        "this_week": this_week,
        "prev_week": prev_week,
        "improvement": improvement,
    }


def _calculate_consistency(completions, today):
    """Calculate workout consistency over last 30 days."""
    month_start = today - timedelta(days=29)
    days_with_activity = (
        completions.filter(completed_at__date__gte=month_start)
        .values("completed_at__date")
        .distinct()
        .count()
    )

    percentage = round((days_with_activity / 30) * 100, 1)
    return {"percentage": percentage, "active_days": days_with_activity}


def _calculate_xp_last_30_days(completions, today):
    """Calculate total XP earned in last 30 days."""
    month_start = today - timedelta(days=29)
    total = (
        completions.filter(completed_at__date__gte=month_start).aggregate(
            total=Sum("xp_earned")
        )["total"]
        or 0
    )
    return {"total": total}


def _calculate_monthly_challenge(completions, profile, today):
    """Calculate monthly challenge progress."""
    target = getattr(profile, "monthly_challenge_target", 20)
    completed = completions.filter(completed_at__date__gte=today.replace(day=1)).count()

    _, days_in_month = calendar.monthrange(today.year, today.month)
    days_left = (today.replace(day=days_in_month) - today).days

    return {
        "description": f"Complete {target} workouts this month",
        "completed": completed,
        "target": target,
        "daysLeft": days_left,
    }


def _calculate_current_streak(completions, today):
    """Calculate consecutive days streak up to today."""
    completion_dates = set(completions.values_list("completed_at__date", flat=True))

    streak = 0
    current_day = today
    while current_day in completion_dates:
        streak += 1
        current_day -= timedelta(days=1)

    return streak


# Analytics


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_weekly_activity(request):
    """
    Return last 7 days of activity for the authenticated user.
    Response: [{ label, date, count, height, isActive }, ...]
    height is a normalized integer 20-100 for frontend bar rendering.
    """
    user_profile = request.user.userprofile
    today = timezone.localdate()
    counts = []

    # collect counts per day (oldest -> newest)
    for days_ago in range(6, -1, -1):
        d = today - timedelta(days=days_ago)
        cnt = WorkoutDayCompletion.objects.filter(
            user_profile=user_profile, completed_at__date=d
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
        result.append(
            {
                "label": d.strftime("%a")[0],  # 'M','T','W','T','F','S','S'
                "date": d.isoformat(),
                "count": cnt,
                "height": height,  # for bar height in UI
                "isActive": cnt > 0,
            }
        )

    return Response(result)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def workout_day_videos(request, id):
    """
    GET: Retrieve all YouTube links for a WorkoutDay
    POST: Add a new YouTube link (coaches only)
    """
    workout_day = get_object_or_404(WorkoutDay, id=id)

    if request.method == "GET":
        return Response({"video_links": workout_day.video_links})

    elif request.method == "POST":
        profile = request.user.userprofile
        if profile.role != "coach":
            raise PermissionDenied("Only coaches can add video links")

        new_link = request.data.get("link")
        if not new_link:
            return Response(
                {"error": "You must provide a YouTube link"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Append new link to JSONField
        workout_day.video_links.append(new_link)
        workout_day.save(update_fields=["video_links"])

        return Response(
            {
                "message": "Video link added",
                "video_links": workout_day.video_links,
            }
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_workout_day_completion(request, id):
    """Check if a workout day is completed by the current user."""
    profile = request.user.userprofile
    workout_day = get_object_or_404(WorkoutDay, pk=id)

    completion = WorkoutDayCompletion.objects.filter(
        user_profile=profile, workout_day=workout_day
    ).first()

    if completion:
        return Response(
            {
                "completed": True,
                "xp_earned": completion.xp_earned,
                "completed_at": completion.completed_at,
            }
        )
    return Response({"completed": False})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def complete_workout_day(request, id):
    """Mark all workouts in a day_number as completed and award XP."""
    profile = request.user.userprofile
    target_day = get_object_or_404(WorkoutDay, pk=id)
    program = target_day.program

    # Get all workouts for this day_number in the program
    same_day_workouts = WorkoutDay.objects.filter(
        program=program, day_number=target_day.day_number
    )

    total_xp = 0
    level = profile.get_current_level()
    workouts_completed_now = 0

    # Complete all workouts in this day
    for workout in same_day_workouts:
        # Skip if already completed
        if WorkoutDayCompletion.objects.filter(
            user_profile=profile, workout_day=workout
        ).exists():
            continue

        # Calculate and award XP
        xp_earned = calculate_xp(
            duration=workout.duration or 30, difficulty_level=program.difficulty_level
        )

        WorkoutDayCompletion.objects.create(
            user_profile=profile, workout_day=workout, xp_earned=xp_earned
        )
        total_xp += xp_earned
        workouts_completed_now += 1

    # Award total XP for the day
    if total_xp > 0:
        level.add_xp(total_xp)

    # Check program completion bonus
    bonus_xp = 0
    leveled_up = False

    # Only check for bonus if we actually completed new workouts
    if workouts_completed_now > 0:
        # Check if ALL day_numbers in program are completed by this user
        total_day_numbers = program.days.values("day_number").distinct().count()
        completed_day_numbers = (
            WorkoutDayCompletion.objects.filter(
                user_profile=profile, workout_day__program=program
            )
            .values("workout_day__day_number")
            .distinct()
            .count()
        )

        program_just_completed = completed_day_numbers >= total_day_numbers

        if profile.role == "member":
            member_obj = getattr(profile, "member_profile", None)
            if member_obj:
                assignment = WorkoutAssignment.objects.filter(
                    member=member_obj, program=program
                ).first()

                if assignment:
                    was_completed = assignment.status == "completed"
                    is_complete = assignment.check_completion()

                    # Award bonus only on first completion
                    if is_complete and not was_completed:
                        bonus_xp = COMPLETION_BONUS
                        leveled_up, prev_rank, new_rank = level.add_xp(bonus_xp)

        elif profile.role == "normal":
            if program_just_completed:
                # Check if we already awarded bonus for this program by
                # checking if completion count matches total days
                already_awarded = getattr(profile, f"bonus_program_{program.id}", False)

                if not already_awarded:
                    bonus_xp = COMPLETION_BONUS
                    leveled_up, prev_rank, new_rank = level.add_xp(bonus_xp)

    level.refresh_from_db()

    return Response(
        {
            "xp_awarded": total_xp,
            "total_xp": level.xp,
            "current_level": level.level,
            "goal_achieved": level.goal_achieved,
            "completed": True,
            "leveled_up": leveled_up,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def workout_progress(request, id):
    profile = request.user.userprofile
    program = get_object_or_404(WorkoutProgram, pk=id)

    total_days = program.days.count()
    completed_qs = WorkoutDayCompletion.objects.filter(
        user_profile=profile, workout_day__program=program
    )
    completed_days = completed_qs.count()
    xp_earned = completed_qs.aggregate(models.Sum("xp_earned"))["xp_earned__sum"] or 0
    return Response(
        {
            "program_id": program.id,
            "program_title": program.title,
            "total_days": total_days,
            "completed_days": completed_days,
            "completion_percentage": (
                round((completed_days / total_days) * 100, 1) if total_days > 0 else 0
            ),
            "xp_earned": xp_earned,
            "completed_day_numbers": list(
                completed_qs.values_list("workout_day__day_number", flat=True)
            ),
        }
    )


# ========== WORKOUT ASSIGNMENT VIEWS ==========


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def workout_assignment_update(request, id):
    """
    Mark assignment completed (member only).
    """
    profile = request.user.userprofile
    if profile.role != "member":
        raise PermissionDenied("Only members can update assignments.")

    assignment = get_object_or_404(WorkoutAssignment, pk=id, member__user=profile)

    if assignment.status == "completed":
        return Response(
            {"message": "This assignment is already completed."}, status=200
        )

    difficulty = assignment.program.difficulty_level
    duration = assignment.program.duration
    xp = calculate_xp(duration=duration, difficulty_level=difficulty)

    assignment.status = "completed"
    assignment.completed_date = timezone.now().date()
    assignment.save(update_fields=["status", "completed_date"])

    # Mark last workout day complete
    last_day = assignment.program.days.order_by("-day_number").first()
    if last_day:
        WorkoutDayCompletion.objects.get_or_create(
            user_profile=profile,
            workout_day=last_day,
            defaults={"xp_earned": xp},
        )

    # Award XP to user
    level = profile.get_current_level()
    level.add_xp(xp)

    return Response(
        {"message": "Assignment completed successfully.", "xp_awarded": xp},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def workout_assignment_detail(request, id):
    profile = request.user.userprofile
    assignment = get_object_or_404(WorkoutAssignment, pk=id)

    # Permissions
    if profile.role == "member" and assignment.member.user != profile:
        raise PermissionDenied("You cannot access this assignment.")
    elif profile.role == "coach":
        if assignment.program.coach != profile:
            raise PermissionDenied("This assignment is not from your programs.")

    serializer = WorkoutAssignmentSerializer(assignment)
    return Response(serializer.data, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_my_assignments(request):
    """
    - Coach sees all their assigned programs
    - Member sees only their own assigned programs
    """
    profile = request.user.userprofile

    if profile.role == "coach":
        assignments = WorkoutAssignment.objects.filter(program__coach=profile)
    elif profile.role == "member":
        assignments = WorkoutAssignment.objects.filter(member__user=profile)
    else:
        assignments = WorkoutAssignment.objects.none()

    serializer = WorkoutAssignmentSerializer(assignments, many=True)
    return Response(serializer.data)
