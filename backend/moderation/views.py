from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from coach.models import Coach
from .models import Admin, AdminModeration

User = get_user_model()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_coach(request, coach_id):
    """Approve a coach certification request."""
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

    return Response(
        {"message": f"Coach {coach.user.user.username} approved."},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reject_coach(request, coach_id):
    """Reject a coach certification request."""
    try:
        coach = Coach.objects.get(pk=coach_id)
    except Coach.DoesNotExist:
        return Response({"error": "Coach not found"}, status=status.HTTP_404_NOT_FOUND)

    admin = Admin.objects.get(user=request.user)
    reason = request.data.get("reason", "Certification rejected")

    coach.status_approval = "rejected"
    coach.save()

    AdminModeration.objects.create(
        admin=admin,
        coach=coach,
        action="reject_certification",
        reason=reason,
    )

    return Response(
        {"message": f"Coach {coach.user.user.username} rejected."},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_coaches_for_admin(request):
    """List all coaches with optional status filter for admin."""
    if not Admin.objects.filter(user=request.user).exists():
        return Response({"error": "You are not an admin"}, status=status.HTTP_403_FORBIDDEN)

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
            "certification_doc": coach.certification_doc.url if coach.certification_doc else None,
            "status_approval": coach.status_approval,
            "created_at": coach.created_at,
        }
        for coach in coaches
    ]

    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_all_users(request):
    """List all users (excluding admins) for admin view."""
    if not Admin.objects.filter(user=request.user).exists():
        return Response({"error": "You are not an admin"}, status=status.HTTP_403_FORBIDDEN)

    users = User.objects.all().order_by("-date_joined")
    data = [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "full_name": u.get_full_name(),
            "role": getattr(u.userprofile, "role", None),
            "date_joined": u.date_joined,
            "is_active": u.is_active,
        }
        for u in users if getattr(u.userprofile, "role", None) != "admin"
    ]

    return Response(data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    """Delete a user account, send email, and log moderation action."""
    try:
        admin = Admin.objects.get(user=request.user)
    except Admin.DoesNotExist:
        return Response({"error": "You are not an admin"}, status=status.HTTP_403_FORBIDDEN)

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Send deletion email
    subject = "Account Deletion Notification"
    message = (
        f"Dear {user.username},\n\n"
        "Your HealthQuest account has been permanently deleted by an administrator.\n\n"
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

    # Log moderation
    AdminModeration.objects.create(
        admin=admin,
        content_type="user",
        content_id=user.id,
        action="delete_user",
        reason="Account deleted by admin",
    )

    username = user.username
    user.delete()

    return Response(
        {"message": f"User '{username}' deleted, email sent, and action logged."},
        status=status.HTTP_200_OK,
    )
