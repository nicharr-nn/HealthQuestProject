from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from coach.models import Coach
from .models import Admin, AdminModeration
from recipe.models import Recipe
from django.shortcuts import get_object_or_404


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_coach(request, coach_id):
    try:
        coach = Coach.objects.get(coach_id=coach_id)
    except Coach.DoesNotExist:
        return Response({"error": "Coach not found"}, status=status.HTTP_404_NOT_FOUND)

    admin = Admin.objects.get(user=request.user)

    coach.status_approval = "approved"
    coach.approved_date = timezone.now()
    coach.save()

    AdminModeration.objects.create(
        admin=admin,
        coach=coach,
        action="approve_certification",
        reason=request.data.get("reason", "Certification approved"),
    )

    return Response({"message": f"Coach {coach.user.user.username} approved."})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reject_coach(request, coach_id):
    try:
        coach = Coach.objects.get(pk=coach_id)
    except Coach.DoesNotExist:
        return Response({"error": "Coach not found"}, status=status.HTTP_404_NOT_FOUND)

    admin = Admin.objects.get(user=request.user)
    reason = request.data.get("reason", "")

    coach.status_approval = "rejected"
    coach.save()

    AdminModeration.objects.create(
        admin=admin,
        coach=coach,
        action="reject_certification",
        reason=reason or "Certification rejected",
    )

    return Response({"message": f"Coach {coach.user.user.username} rejected."})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_coaches_for_admin(request):
    if not Admin.objects.filter(user=request.user).exists():
        return Response({"error": "You are not an admin"}, status=403)

    status_filter = request.query_params.get("status")
    coaches = Coach.objects.all().select_related("user__user")
    if status_filter in ["pending", "approved", "rejected"]:
        coaches = coaches.filter(status_approval=status_filter)

    data = [
        {
            "coach_id": coach.coach_id,
            "name": coach.user.user.get_full_name() or coach.user.user.username,
            "email": coach.user.user.email,
            "bio": getattr(coach, "bio", ""),
            "certification_doc": (
                coach.certification_doc.url if coach.certification_doc else None
            ),
            "status_approval": coach.status_approval,
            "created_at": coach.created_at,
        }
        for coach in coaches
    ]
    return Response(data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id)
    user_profile = request.user.userprofile
    is_admin = hasattr(request.user, "admin")

    if recipe.user_profile != user_profile and not is_admin:
        return Response(
            {"detail": "Permission denied. You can only delete your own recipes."},
            status=status.HTTP_403_FORBIDDEN,
        )

    recipe.delete()
    return Response({"detail": "Recipe deleted successfully."}, status=200)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_workout(request, id):
    from workout.models import WorkoutProgram

    workout = get_object_or_404(WorkoutProgram, pk=id)
    user_profile = request.user.userprofile
    is_admin = hasattr(request.user, "admin")

    if workout.coach.user != user_profile and not is_admin:
        return Response(
            {"detail": "Permission denied. You can only delete your own workouts."},
            status=status.HTTP_403_FORBIDDEN,
        )

    workout.delete()
    return Response({"detail": "Workout deleted successfully."}, status=200)
