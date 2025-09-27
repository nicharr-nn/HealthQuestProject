from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import UserProfileSerializer, UserSerializer, WorkoutProgramSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .xp_rules import calculate_xp
from django.apps import apps
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .models import WorkoutProgram, WorkoutAssignment, WorkoutCompletion, Achievement, UserAchievement, FoodPost


User = get_user_model()

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
def set_goal(request):
    """Set user fitness goal"""
    from django.apps import apps

    FitnessGoal = apps.get_model("users", "FitnessGoal")

    try:
        profile = request.user.userprofile

        # Only normal users can have fitness goals
        if profile.role != "normal":
            return Response(
                {"detail": "Only normal users can set fitness goals."}, status=400
            )

        goal_type = request.data.get("goal_type")
        end_date = request.data.get("end_date")

        if not goal_type:
            return Response({"detail": "Goal type is required."}, status=400)

        # Create new FitnessGoal
        FitnessGoal.objects.create(
            user_profile=profile, goal_type=goal_type, end_date=end_date
        )

        # Serialize the updated user profile
        from .serializers import UserSerializer

        serializer = UserSerializer(request.user)

        return Response({"status": "success", "user": serializer.data})

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

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail(request, id):
    """Retrieve, update, or deactivate user account"""
    if request.user.id != id:
        return Response({"detail": "Not authorized."}, status=403)

    user = get_object_or_404(User, pk=id)

    if request.method == "GET":
        return Response(UserSerializer(user).data)

    elif request.method in ["PUT", "PATCH"]:
        profile = getattr(user, "userprofile", None)
        if not profile:
            return Response({"error": "Profile not found"}, status=404)

        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        user.profile_complete = False
        user.save()
        return Response({"message": "Account deactivated"})

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

    if request.method == "PATCH":  # mark complete
        xp = calculate_xp(assignment.program.difficulty, assignment.program.duration_minutes)
        assignment.status = "completed"
        assignment.completed_date = timezone.now()
        assignment.save()

        # Log completion
        WorkoutCompletion.objects.create(
            assignment=assignment, user_profile=profile, xp_earned=xp
        )

        # Update user XP
        ul = profile.get_current_level()
        ul.add_xp(xp)

        return Response({"message": "Assignment completed", "xp_awarded": xp})

    elif request.method == "DELETE":
        assignment.delete()
        return Response({"message": "Assignment deleted"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def achievements(request):
    """List all achievements"""
    data = Achievement.objects.all().values("id", "title", "description", "xp_reward")
    return Response(list(data))

@api_view(['GET, DELETE'])
@permission_classes([IsAuthenticated])
def user_achievements(request):
    """get or remove an achievement for the authenticated user"""
    profile = request.user.userprofile

    if request.method == "GET":
        achievements = UserAchievement.objects.filter(user_profile=profile).select_related("achievement")
        data = [{"id": ua.id, "date_earned": ua.date_earned} for ua in achievements]
        return Response(data)

    elif request.method == "DELETE":
        ach_id = request.data.get("achievement_id")
        ua = get_object_or_404(UserAchievement, pk=ach_id, user_profile=profile)
        ua.delete()
        return Response({"message": "Achievement removed"})

@api_view(['GET, POST'])
@permission_classes([IsAuthenticated])
def food_posts(request):
    """List or create food posts"""
    if request.method == "GET":
        posts = FoodPost.objects.all().select_related("user_profile")
        data = [{"id": p.id, "title": p.title, "description": p.description, "author": p.user_profile.user.username} for p in posts]
        return Response(data)

    elif request.method == "POST":
        profile = request.user.userprofile
        post = FoodPost.objects.create(
            user_profile=profile,
            title=request.data.get("title"),
            description=request.data.get("description"),
        )
        return Response({"message": "Post created", "post_id": post.id})

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def food_post_comment(request, id):
#     """Add a comment to a food post"""
#     profile = request.user.userprofile
#     post = get_object_or_404(FoodPost, pk=id)

#     comment = FoodPostComment.objects.create(
#         post=post, user_profile=profile, content=request.data.get("content")
#     )
#     return Response({"message": "Comment added", "comment_id": comment.id})

@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def food_post_update(request, id):
    """update or delete to a food post"""
    profile = request.user.userprofile
    post = get_object_or_404(FoodPost, pk=id, user_profile=profile)

    if request.method in ["PUT", "PATCH"]:
        post.title = request.data.get("title", post.title)
        post.description = request.data.get("description", post.description)
        post.save()
        return Response({"message": "Post updated"})

    elif request.method == "DELETE":
        post.delete()
        return Response({"message": "Post deleted"})