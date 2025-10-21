from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

from users.models import UserProfile
from workout.models import WorkoutProgram, WorkoutDayCompletion
from .models import WorkoutAssignment
from .serializers import WorkoutAssignmentSerializer
from workout.xp_rules import calculate_xp, COMPLETION_BONUS


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def assign_program_to_member(request, id):
    """
    Assign a workout program to a member (coaches only).
    Endpoint: POST /api/member/assign/<member_id>/
    """
    coach_profile = request.user.userprofile
    if coach_profile.role != "coach":
        raise PermissionDenied("Only coaches can assign programs.")

    member = get_object_or_404(UserProfile, pk=id)
    if member.role != "member":
        return Response({"error": "Target user is not a member."}, status=status.HTTP_400_BAD_REQUEST)

    program_id = request.data.get("program_id")
    if not program_id:
        return Response({"error": "Program ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    program = get_object_or_404(WorkoutProgram, pk=program_id)

    assignment = WorkoutAssignment.objects.create(
        user_profile=member,
        program=program,
    )

    serializer = WorkoutAssignmentSerializer(assignment)
    return Response({"message": "Program assigned successfully.", "assignment": serializer.data},
                    status=status.HTTP_201_CREATED)


@api_view(["PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def workout_assignment_update(request, id):
    """
    PATCH: Mark assignment completed (member only).
    DELETE: Delete assignment (member only).
    Endpoint: /api/member/assignments/<id>/
    """
    profile = request.user.userprofile
    assignment = get_object_or_404(WorkoutAssignment, pk=id, user_profile=profile)

    if profile.role != "member":
        raise PermissionDenied("Only members can modify their assignments.")

    if request.method == "PATCH":
        difficulty = assignment.program.difficulty_level
        duration = assignment.program.duration
        xp = calculate_xp(duration=duration, difficulty_level=difficulty)

        # Mark assignment complete
        assignment.status = "completed"
        assignment.completed_date = timezone.now().date()
        assignment.save(update_fields=["status", "completed_date"])

        # Ensure last workout day is marked complete
        last_day = assignment.program.days.order_by("-day_number").first()
        if last_day:
            WorkoutDayCompletion.objects.get_or_create(
                user_profile=profile,
                workout_day=last_day,
                defaults={"xp_earned": xp},
            )

        # Award XP
        ul = profile.get_current_level()
        ul.add_xp(xp)

        return Response(
            {"message": "Assignment completed successfully.", "xp_awarded": xp},
            status=status.HTTP_200_OK
        )

    elif request.method == "DELETE":
        assignment.delete()
        return Response({"message": "Assignment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def todays_workout(request):
    profile = request.user.userprofile
    # choose the next active assignment for the user
    assignment = (
        WorkoutAssignment.objects.filter(user_profile=profile, status="assigned")
        .order_by("created_at")
        .first()
    )
    if not assignment:
        return Response({"message": "No active assignment"}, status=200)
    program = assignment.program
    # return basic program + assignment id
    return Response(
        {
            "assignment_id": assignment.id,
            "program": {
                "id": program.id,
                "name": program.name,
                "description": program.description,
                "duration": program.duration,
                "difficulty_level": program.difficulty_level,
                "xp": program.xp if hasattr(program, "xp") else None,
            },
        }
    )
