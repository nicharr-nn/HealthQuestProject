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
        xp = calculate_xp(difficulty, duration)

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
