from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.apps import apps

from .serializers import UserProfileSerializer, UserSerializer

User = get_user_model()


@api_view(["GET"])
@permission_classes([AllowAny])  # allow GET without auth
def user_info(request):
    """
    Return user info and authentication status.
    """
    user = request.user

    if request.method == "GET":
        if user.is_authenticated:
            serializer = UserSerializer(user)
            return Response({"isAuthenticated": True, "user": serializer.data})
        else:
            return Response({"isAuthenticated": False, "user": None})


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_account(request):
    """Delete user account"""
    user = request.user

    if request.method == "DELETE":
        # require user_id for security
        user_id = request.data.get("user_id")

        if user_id is None:
            return Response(
                {"detail": "User ID is required for account deletion."}, status=400
            )

        # Verify it matches authenticated user
        if str(user.id) != str(user_id):
            return Response(
                {"detail": "You can only delete your own account."}, status=403
            )

        # User is authenticated and owns the account
        user.delete()
        return Response({"message": "Account deleted permanently"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_role(request):
    """Set user role"""
    from .models import UserProfile

    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.role = request.data.get("role")
        profile.save()
        return Response({"status": "success", "role": profile.role})
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Update user profile data"""
    try:
        profile = request.user.userprofile
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response({"status": "error", "errors": serializer.errors}, status=400)

    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_photo(request):
    """Handle profile photo upload for authenticated users"""
    if "photo" not in request.FILES:
        return Response({"detail": "No file provided."}, status=400)

    photo = request.FILES["photo"]
    file_path = default_storage.save(
        f"profile_photos/{photo.name}", ContentFile(photo.read())
    )

    user = request.user
    if hasattr(user, "userprofile"):
        user.userprofile.photo = file_path
        user.userprofile.save()

    full_url = request.build_absolute_uri(default_storage.url(file_path))

    return Response(
        {
            "detail": "Photo uploaded successfully!",
            "file_path": file_path,
            "photo_url": full_url,
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_goal(request):
    """Set user fitness goal"""

    FitnessGoal = apps.get_model("users", "FitnessGoal")

    try:
        profile = request.user.userprofile

        # Only normal users and members can have fitness goals
        if profile.role != "normal" and profile.role != "member":
            return Response(
                {"detail": "Only normal users and members can set fitness goals."},
                status=400,
            )

        goal_type = request.data.get("goal_type")
        end_date = request.data.get("end_date")

        if not goal_type:
            return Response({"detail": "Goal type is required."}, status=400)

        # Create new FitnessGoal
        FitnessGoal.objects.update_or_create(
            user_profile=profile, goal_type=goal_type, end_date=end_date
        )

        # Serialize the updated user profile

        serializer = UserSerializer(request.user)

        return Response({"status": "success", "user": serializer.data})

    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_levels(request):
    profile = getattr(request.user, "userprofile", None)
    if not profile:
        return Response({"detail": "Profile not found"}, status=400)
    current = (
        profile.get_current_level() if hasattr(profile, "get_current_level") else None
    )

    next_xp = 1000 if current and current.level_rank == 1 else None
    payload = {
        "current": (
            {
                "level": current.level,
                "level_rank": current.level_rank,
                "xp": current.xp,
            }
            if current
            else None
        ),
        "next_xp": next_xp,
    }
    return Response(payload)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def all_users(request):
    # exclude admin users
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
