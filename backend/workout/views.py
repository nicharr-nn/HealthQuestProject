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
from .models import WorkoutProgram, WorkoutAssignment, WorkoutDayCompletion, WorkoutDay
from django.utils import timezone
from users.serializers import UserSerializer
from django.db import models

User = get_user_model()

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def workout_programs(request):
    if request.method == 'GET':
        programs = WorkoutProgram.objects.all()
        serializer = WorkoutProgramSerializer(programs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if request.user.userprofile.role != "coach":
            raise PermissionDenied("Only coaches can create programs")
        serializer = WorkoutProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def workout_program_detail(request, id):
    program = get_object_or_404(WorkoutProgram, pk=id)

    if request.method == 'GET':
        serializer = WorkoutProgramSerializer(program)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user.userprofile.role != "coach":
            raise PermissionDenied("Only coaches can update programs")
        serializer = WorkoutProgramSerializer(program, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if request.user.userprofile.role != "coach" or program.coach != request.user.userprofile:
            raise PermissionDenied("Only the owning coach can delete this program")
        program.delete()
        return Response({"message": "Program deleted"})


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

        #  mark last day of program complete
        last_day = assignment.program.days.order_by("-day_number").first()
        if last_day:
            WorkoutDayCompletion.objects.get_or_create(
                user_profile=profile,
                workout_day=last_day,
                defaults={"xp_earned": xp}
            )

        # Update user XP
        ul = profile.get_current_level()
        ul.add_xp(xp)

        return Response({"message": "Assignment completed", "xp_awarded": xp})

    elif request.method == "DELETE":
        assignment.delete()
        return Response({"message": "Assignment deleted"})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def workout_day_videos(request, id):
    """
    GET: Retrieve all YouTube links for a WorkoutDay
    POST: Add a new YouTube link (coaches only)
    """
    workout_day = get_object_or_404(WorkoutDay, id=id)

    if request.method == 'GET':
        return Response({"video_links": workout_day.video_links})

    elif request.method == 'POST':
        profile = request.user.userprofile
        if profile.role != "coach":
            raise PermissionDenied("Only coaches can add video links")

        new_link = request.data.get("link")
        if not new_link:
            return Response({"error": "You must provide a YouTube link"}, status=status.HTTP_400_BAD_REQUEST)

        # Append new link to JSONField
        workout_day.video_links.append(new_link)
        workout_day.save(update_fields=["video_links"])

        return Response({"message": "Video link added", "video_links": workout_day.video_links})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_workout_day(request, id):
    profile = request.user.userprofile

    workout_day = get_object_or_404(WorkoutDay, pk=id)

    # calculate XP for this workout day
    xp_value = calculate_xp(
        duration=workout_day.duration,
        difficulty_level=workout_day.program.difficulty_level
    )

    completion, created = WorkoutDayCompletion.objects.get_or_create(
        user_profile=profile,
        workout_day=workout_day,
        defaults={"xp_earned": xp_value}
    )
    if not created:
        return Response({"message": "Already completed"})

    # award XP
    profile.get_current_level().add_xp(xp_value)

    # Case 1: Member with assignment → check if program is now complete
    if profile.role == "member":
        assignments = WorkoutAssignment.objects.filter(
            user_profile=profile, program=workout_day.program
        )
        for assignment in assignments:
            assignment.check_completion()

    # Case 2: Normal user → no assignment, just track progress with completions
    # (streaks and XP already handled)

    return Response({
        "message": "Workout day completed",
        "xp": xp_value,
        "day": workout_day.day_number,
        "program": workout_day.program.title
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def workout_progress(request, program_id):
    profile = request.user.userprofile
    program = get_object_or_404(WorkoutProgram, pk=program_id)

    total_days = program.days.count()
    completed_qs = WorkoutDayCompletion.objects.filter(
        user_profile=profile,
        workout_day__program=program
    )
    completed_days = completed_qs.count()
    xp_earned = completed_qs.aggregate(models.Sum("xp_earned"))["xp_earned__sum"] or 0

    return Response({
        "program_id": program.id,
        "program_title": program.title,
        "total_days": total_days,
        "completed_days": completed_days,
        "completion_percentage": round((completed_days / total_days) * 100, 1) if total_days > 0 else 0,
        "xp_earned": xp_earned,
        "completed_day_numbers": list(completed_qs.values_list("workout_day__day_number", flat=True))
    })


