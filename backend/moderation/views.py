from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from coach.models import Coach
from .models import Admin
from recipe.models import Recipe
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_coach(request, coach_id):
    # Check admin
    try:
        admin = Admin.objects.get(user=request.user)
    except Admin.DoesNotExist:
        return Response(
            {"error": "You do not have permission to approve coaches."},
            status=status.HTTP_403_FORBIDDEN
        )

    # Find the coach
    try:
        coach = Coach.objects.get(pk=coach_id)
    except Coach.DoesNotExist:
        return Response(
            {"error": "Coach not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Approve the coach
    coach.status_approval = "approved"
    coach.approved_date = timezone.now()
    coach.save()

    return Response(
        {"message": f"Coach {coach.user.user.username} approved."},
        status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reject_coach(request, coach_id):
    # Check admin
    try:
        admin = Admin.objects.get(user=request.user)
    except Admin.DoesNotExist:
        return Response(
            {"error": "You do not have permission to reject coaches."},
            status=status.HTTP_403_FORBIDDEN
        )

    # Find coach
    try:
        coach = Coach.objects.get(pk=coach_id)
    except Coach.DoesNotExist:
        return Response(
            {"error": "Coach not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Reject coach
    coach.status_approval = "rejected"
    coach.save()

    return Response(
        {"message": f"Coach {coach.user.user.username} rejected."},
        status=status.HTTP_200_OK
    )


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
            "name": (
                coach.user.user.get_full_name() or
                coach.user.user.username
            ),
            "email": coach.user.user.email,
            "bio": getattr(coach, "bio", ""),
            "certification_doc": (
                coach.certification_doc.url
                if coach.certification_doc
                else None
            ),
            "status_approval": coach.status_approval,
            "created_at": coach.created_at,
        }
        for coach in coaches
    ]
    return Response(data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    user_profile = request.user.userprofile
    is_admin = hasattr(request.user, "admin_profile")

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
    is_admin = hasattr(request.user, "admin_profile")

    if workout.coach != user_profile and not is_admin:
        return Response(
            {"detail": "Permission denied. You can only delete your own workouts."},
            status=status.HTTP_403_FORBIDDEN,
        )

    workout.delete()
    return Response({"detail": "Workout deleted successfully."}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_all_users(request):
    # Check admin permission
    if not Admin.objects.filter(user=request.user).exists():
        return Response({"error": "You are not an admin"}, status=403)

    users = User.objects.all().order_by("-date_joined")

    data = [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "full_name": u.get_full_name(),
            "role": getattr(u.userprofile, "role", None),
            "photo": (
                request.build_absolute_uri(u.userprofile.photo.url)
                if hasattr(u, "userprofile") and u.userprofile.photo
                else None
            ),
            "date_joined": u.date_joined,
            "is_active": u.is_active,
        }
        for u in users if u.userprofile.role != "admin"
    ]

    return Response(data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    try:
        admin = Admin.objects.get(user=request.user)
    except Admin.DoesNotExist:
        return Response(
            {"error": "You are not an admin"},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    subject = "Account Deletion Notification"
    message = (
        f"Dear {user.username},\n\n"
        "Your HealthQuest account has been "
        "permanently deleted by an administrator.\n\n\n"
        "Thank you,\n"
        "HealthQuest Team"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

    username = user.username
    user.delete()

    return Response(
        {
            "message": (
                f"User '{username}' deleted, "
                "email sent and action logged."
            )
        },
        status=status.HTTP_200_OK,
    )
