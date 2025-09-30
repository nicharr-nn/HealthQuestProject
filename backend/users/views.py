from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import UserProfileSerializer, UserSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


@api_view(["GET", "PUT", "PATCH"])
@permission_classes([AllowAny])  # allow GET without auth, require auth for PUT/PATCH
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

    elif request.method in ["PUT", "PATCH"]:
        if not user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=401)

        serializer = UserSerializer(
            user, data=request.data, partial=(request.method == "PATCH")
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"isAuthenticated": True, "user": serializer.data})
        return Response(serializer.errors, status=400)


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
