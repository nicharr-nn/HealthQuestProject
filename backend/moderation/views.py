from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from coach.models import Coach
from .models import Admin, AdminModeration
from member.models import Member
from django.contrib.auth import get_user_model

User = get_user_model()


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
            "date_joined": u.date_joined,
            "is_active": u.is_active,
        }
        for u in users
    ]

    return Response(data)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    if not Admin.objects.filter(user=request.user).exists():
        return Response({"error": "Unauthorized"}, status=403)

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    user.delete()
    return Response({"message": "User deleted"}, status=200)
