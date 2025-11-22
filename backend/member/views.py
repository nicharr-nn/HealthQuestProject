from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Member, CoachMemberRelationship, FoodPost, FoodPostComment
from django.shortcuts import get_object_or_404
from .serializers import (
    CoachMemberRelationshipSerializer,
    MemberSerializer,
    FoodPostSerializer,
    FoodPostCommentSerializer,
)
from coach.models import Coach
from workout.models import WorkoutProgram, WorkoutAssignment, WorkoutDayCompletion
from workout.serializers import WorkoutAssignmentSerializer
from django.db import models


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def coach_member_profile(request, member_id):
    """Allow a coach to view the profile of a member they are connected to."""
    user_profile = getattr(request.user, "userprofile", None)
    coach_profile = getattr(user_profile, "coach_profile", None)

    if not coach_profile:
        return Response(
            {"error": "You are not a coach"}, status=status.HTTP_403_FORBIDDEN
        )

    member = get_object_or_404(Member, member_id=member_id)

    # Ensure this coach has a relationship with the member
    if not CoachMemberRelationship.objects.filter(
        coach=coach_profile, member=member
    ).exists():
        return Response(
            {"error": "You do not have access to this member."},
            status=status.HTTP_403_FORBIDDEN,
        )

    profile = member.user
    user = profile.user

    # Calculate progress if member has assignments
    total_days = 0
    completed_days = 0
    progress = 0
    assignments = WorkoutAssignment.objects.filter(member=member).select_related(
        "program"
    )
    if assignments.exists():
        for assignment in assignments:
            program_days = (
                assignment.program.days.values("day_number").distinct().count()
            )
            total_days += program_days
            program_completed = (
                WorkoutDayCompletion.objects.filter(
                    user_profile=profile, workout_day__program=assignment.program
                )
                .values("workout_day__day_number")
                .distinct()
                .count()
            )
            completed_days += program_completed
        if total_days > 0:
            progress = round((completed_days / total_days) * 100, 1)

    data = {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
        "age": profile.age,
        "gender": profile.gender,
        "height": profile.height,
        "weight": profile.weight,
        "location": profile.location,
        "photo": profile.photo.url if profile.photo else None,
        "experienceLevel": member.experience_level,
        "programName": member.program_name,
        "joinedAt": member.submitted_at,
        "message": member.message,
        "progress": progress,
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def coach_member_requests(request, pk=None):
    user_profile = getattr(request.user, "userprofile", None)
    coach_profile = getattr(user_profile, "coach_profile", None)

    if not coach_profile:
        return Response(
            {"error": "You are not a coach"}, status=status.HTTP_403_FORBIDDEN
        )

    if pk:
        try:
            relationship = CoachMemberRelationship.objects.get(
                pk=pk, coach=coach_profile
            )
        except CoachMemberRelationship.DoesNotExist:
            return Response(
                {"error": "Request not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.method == "PATCH":
            new_status = request.data.get("status")
            if new_status:
                relationship.status = new_status
                relationship.save()

                # When coach accepts, also activate the member
                member = relationship.member
                if new_status in ["accepted", "approved"]:
                    # Update member status to approve
                    if hasattr(member, "status"):
                        member.status = "approved"
                        member.save()

                elif new_status == "rejected":
                    # Optionally reset member to pending or inactive
                    if hasattr(member, "status"):
                        member.status = "pending"
                        member.save()

        serializer = CoachMemberRelationshipSerializer(relationship)
        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        relationships = CoachMemberRelationship.objects.filter(coach=coach_profile)
        serializer = CoachMemberRelationshipSerializer(relationships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def accepted_members(request):
    user_profile = getattr(request.user, "userprofile", None)
    coach_profile = getattr(user_profile, "coach_profile", None)

    if not coach_profile:
        return Response(
            {"error": "You are not a coach"}, status=status.HTTP_403_FORBIDDEN
        )

    relationships = CoachMemberRelationship.objects.filter(
        coach=coach_profile, status__in=["accepted", "approved"]
    ).select_related("member__user__user")

    # convert to frontend format (including profile photo)
    members_data = []
    for r in relationships:
        profile = r.member.user  # UserProfile
        user = profile.user
        photo_url = None
        if getattr(profile, "photo", None):
            if hasattr(profile.photo, "url"):
                photo_url = profile.photo.url
            else:
                photo_url = str(profile.photo)

        members_data.append(
            {
                "memberId": r.member.member_id,
                "name": user.get_full_name() or user.username,
                "programName": r.member.program_name,
                "joinedAt": r.member.submitted_at,
                "experienceLevel": r.member.experience_level,
                "member_photo": photo_url,
            }
        )

    return Response(members_data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def coach_remove_member(request, member_id):
    """Allow a coach to remove an accepted member from their list."""
    user_profile = getattr(request.user, "userprofile", None)
    coach_profile = getattr(user_profile, "coach_profile", None)

    if not coach_profile:
        return Response(
            {"error": "You are not a coach"}, status=status.HTTP_403_FORBIDDEN
        )

    member = get_object_or_404(Member, member_id=member_id)

    try:
        relationship = CoachMemberRelationship.objects.get(
            coach=coach_profile, member=member
        )
    except CoachMemberRelationship.DoesNotExist:
        return Response(
            {"error": "Relationship not found"}, status=status.HTTP_404_NOT_FOUND
        )

    relationship.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ==================== MEMBER ENDPOINTS ====================
@api_view(["POST", "PATCH"])
@permission_classes([IsAuthenticated])
def apply_as_member(request):
    """
    Create or update a Member profile for the authenticated user.
    Members can use public_id (like C_A1B2C3D4) to request coaches.
    """
    profile = request.user.userprofile

    # Ensure role is 'member'
    if profile.role != "member":
        profile.role = "member"
        profile.save()

    # Create or update member profile
    member, created = Member.objects.get_or_create(
        user=profile,
        defaults={
            "experience_level": request.data.get("experience_level", "beginner"),
            "program_name": None,
            "message": request.data.get("message", ""),
            "member_id": f"M-{profile.user.id:05d}",
        },
    )

    # Update fields if PATCH or if already exists
    if not created or request.method == "PATCH":
        member.experience_level = request.data.get(
            "experience_level", member.experience_level
        )
        member.message = request.data.get("message", member.message)
        member.save()

    coach_code = request.data.get("coach_code")
    if coach_code:
        try:
            # Try to find coach by public_id first
            if coach_code.startswith("C-"):
                coach = Coach.objects.get(public_id=coach_code)
            else:
                # Fallback: try primary key or username
                try:
                    # Try as primary key
                    coach = Coach.objects.get(pk=int(coach_code))
                except (ValueError, Coach.DoesNotExist):
                    # Try as username
                    coach = Coach.objects.get(user__user__username=coach_code)

            # Check if relationship already exists
            existing_relationship = CoachMemberRelationship.objects.filter(
                member=member
            ).first()

            if existing_relationship:
                current_coach_name = existing_relationship.coach.user.user.username
                return Response(
                    {
                        "error": f"You already have a {existing_relationship.status} "
                        f"relationship with coach {current_coach_name}. "
                        f"Please cancel it first to request a new coach."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create new relationship
            relationship = CoachMemberRelationship.objects.create(
                coach=coach, member=member, status="pending"
            )

            # Return success response with coach info
            return Response(
                {
                    "message": f"Request sent to {coach.user.user.username}!",
                    "member": MemberSerializer(member).data,
                    "coach": {
                        "name": coach.user.user.username,
                        "public_id": coach.public_id,
                    },
                    "status": "pending",
                    "relationship_id": relationship.relationship_id,
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            )

        except Coach.DoesNotExist:
            # Provide helpful error message with available coaches
            available_coaches = Coach.objects.filter(status_approval="approved")[:5]
            coach_list = [
                {
                    "public_id": coach.public_id,
                    "name": coach.user.user.username,
                }
                for coach in available_coaches
            ]

            return Response(
                {
                    "error": f"Coach with code '{coach_code}' not found.",
                    "available_coaches": coach_list,
                    "hint": "Try one of these available coach codes",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to create relationship: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    return Response(
        MemberSerializer(member).data,
        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_member_profile(request):
    """
    Retrieve the Member profile for the authenticated user.
    """
    profile = request.user.userprofile

    try:
        member = Member.objects.get(user=profile)
        serializer = MemberSerializer(member)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Member.DoesNotExist:
        return Response(
            {"error": "Member profile not found."},
            status=status.HTTP_404_NOT_FOUND,
        )


# helper function
def _update_member_program_name(member):
    """Update member's program_name to reflect active assignment"""

    active_assignment = (
        WorkoutAssignment.objects.filter(
            member=member, status__in=["in_progress", "assigned", "paused"]
        )
        .order_by(
            models.Case(
                models.When(status="in_progress", then=1),
                models.When(status="assigned", then=2),
                models.When(status="paused", then=3),
                default=99,
            )
        )
        .first()
    )

    if active_assignment:
        member.program_name = active_assignment.program.title
    else:
        member.program_name = None
    member.save(update_fields=["program_name"])


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def manage_member_request(request):
    """
    Member can:
      - GET: view their coach request(s)
      - PATCH: update their message or experience_level
      - DELETE: cancel the request
    """
    profile = request.user.userprofile

    try:
        member = Member.objects.get(user=profile)
    except Member.DoesNotExist:
        return Response(
            {"error": "You are not a member."}, status=status.HTTP_404_NOT_FOUND
        )

    try:
        relationship = CoachMemberRelationship.objects.get(member=member)
    except CoachMemberRelationship.DoesNotExist:
        return Response(
            {"message": "No coach request found."}, status=status.HTTP_200_OK
        )

    if request.method == "GET":
        _update_member_program_name(member)
        serializer = CoachMemberRelationshipSerializer(relationship)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PATCH":
        new_message = request.data.get("message")
        new_level = request.data.get("experience_level")

        if new_message:
            member.message = new_message
        if new_level:
            member.experience_level = new_level
        member.save()

        serializer = MemberSerializer(member)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # DELETE (cancel request)
    elif request.method == "DELETE":
        relationship.delete()
        return Response(
            {"message": "Your coach request has been cancelled."},
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def assign_program_to_member(request):
    """
    Assign a workout program to a member (coaches only).
    """
    coach_profile = request.user.userprofile
    if coach_profile.role != "coach":
        return Response(
            {"error": "Only coaches can assign programs."},
            status=status.HTTP_403_FORBIDDEN,
        )

    member_identifier = request.data.get("member_id")
    if not member_identifier:
        return Response(
            {"error": "Member ID is required."}, status=status.HTTP_400_BAD_REQUEST
        )

    program_id = request.data.get("program_id")
    if not program_id:
        return Response(
            {"error": "Program ID is required."}, status=status.HTTP_400_BAD_REQUEST
        )

    # Try to find member by member_id string first, then by primary key
    try:
        if isinstance(member_identifier, str) and member_identifier.startswith("M-"):
            member = Member.objects.get(member_id=member_identifier)
        else:
            # Try as primary key
            member = Member.objects.get(pk=member_identifier)
    except Member.DoesNotExist:
        return Response(
            {"error": "Member not found."}, status=status.HTTP_404_NOT_FOUND
        )

    program = get_object_or_404(WorkoutProgram, pk=program_id)

    # Optional due date
    due_date = request.data.get("due_date")

    if due_date:
        try:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
            if due_date_obj <= datetime.now().date():
                return Response(
                    {"error": "Due date must be in the future"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValueError:
            return Response(
                {"error": "Invalid due date format. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Prevent duplicates
    if WorkoutAssignment.objects.filter(member=member, program=program).exists():
        return Response(
            {"message": "This program is already assigned to the member."},
            status=status.HTTP_200_OK,
        )

    assignment = WorkoutAssignment.objects.create(
        member=member,
        program=program,
        due_date=due_date if due_date else None,
    )

    member.program_name = program.title
    member.save(update_fields=["program_name"])

    serializer = WorkoutAssignmentSerializer(assignment)
    return Response(
        {"message": "Program assigned successfully.", "assignment": serializer.data},
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def member_assignments(request, member_id):
    """
    Get all workout assignments for a specific member.
    Only accessible by the member's coach.
    """
    try:
        user_profile = request.user.userprofile

        # Check if user is a coach
        if user_profile.role != "coach":
            return Response(
                {"error": "Only coaches can view member assignments"},
                status=status.HTTP_403_FORBIDDEN,
            )

        coach = Coach.objects.get(user=user_profile)

        # Get the member
        try:
            member = Member.objects.get(member_id=member_id)
        except Member.DoesNotExist:
            return Response(
                {"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Verify relationship exists
        relationship = CoachMemberRelationship.objects.filter(
            coach=coach, member=member, status="accepted"
        ).first()

        if not relationship:
            return Response(
                {"error": "You do not have access to this member's assignments"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get all assignments for this member
        assignments = WorkoutAssignment.objects.filter(member=member).select_related(
            "program"
        )

        assignments_data = []
        for assignment in assignments:
            program = assignment.program
            assignments_data.append(
                {
                    "id": assignment.id,
                    "program": {
                        "id": program.id,
                        "title": program.title,
                        "category": program.category,
                        "difficulty_level": program.difficulty_level,
                        "description": program.description,
                    },
                    "status": assignment.status,
                    "assigned_date": assignment.assigned_date,
                }
            )

        return Response(assignments_data, status=status.HTTP_200_OK)

    except Coach.DoesNotExist:
        return Response(
            {"error": "Coach profile not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def coach_member_workout_progress(request, program_id, member_id):
    """
    Coach-specific endpoint to view member's workout progress.
    URL: /api/member/member-progress/<program_id>/<member_id>/
    """
    user_profile = request.user.userprofile

    # Only coaches can access
    if user_profile.role != "coach":
        return Response(
            {"error": "Only coaches can access member progress"},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        coach = Coach.objects.get(user=user_profile)
        program = get_object_or_404(WorkoutProgram, pk=program_id)

        # Get the member
        if member_id.startswith("M-"):
            member = Member.objects.get(member_id=member_id)
        else:
            member = Member.objects.get(pk=member_id)

        # Verify relationship
        relationship = CoachMemberRelationship.objects.filter(
            coach=coach, member=member, status="accepted"
        ).first()

        if not relationship:
            return Response(
                {"error": "You don't have access to this member's progress"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get progress data
        member_profile = member.user
        total_workouts = program.days.count()
        completed_qs = WorkoutDayCompletion.objects.filter(
            user_profile=member_profile, workout_day__program=program
        )
        completed_day_numbers = list(
            completed_qs.values_list("workout_day__day_number", flat=True)
            .distinct()
            .order_by("workout_day__day_number")
        )

        completed_workouts = completed_qs.count()
        xp_earned = (
            completed_qs.aggregate(models.Sum("xp_earned"))["xp_earned__sum"] or 0
        )

        return Response(
            {
                "program_id": program.id,
                "program_title": program.title,
                "member": {
                    "member_id": member.member_id,
                    "name": member_profile.user.first_name
                    or member_profile.user.username,
                },
                "total_workouts": total_workouts,
                "completed_workouts": completed_workouts,
                "completion_percentage": (
                    round((completed_workouts / total_workouts) * 100, 1)
                    if total_workouts > 0
                    else 0
                ),
                "xp_earned": xp_earned,
                "completed_day_numbers": completed_day_numbers,
            }
        )

    except Member.DoesNotExist:
        return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)
    except Coach.DoesNotExist:
        return Response(
            {"error": "Coach profile not found"}, status=status.HTTP_404_NOT_FOUND
        )


# ==================== FOOD POSTS ====================


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def food_posts(request):
    """List or create food posts"""
    profile = request.user.userprofile

    if request.method == "GET":
        if profile.role == "member":
            posts = FoodPost.objects.filter(user_profile=profile)
        elif profile.role == "coach":
            member_id = request.query_params.get("member_id")
            date_str = request.query_params.get("date")

            posts = FoodPost.objects.filter(coach=profile)

            if member_id:
                posts = posts.filter(user_profile__member_profile__member_id=member_id)

            if date_str:
                try:
                    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    posts = posts.filter(created_at__date=target_date)
                except ValueError:
                    # If date is invalid, ignore.
                    pass
        else:
            posts = FoodPost.objects.none()

        serializer = FoodPostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = FoodPostSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def food_post_update(request, id):
    """Update a food post"""
    profile = request.user.userprofile
    post = get_object_or_404(FoodPost, pk=id, user_profile=profile)

    serializer = FoodPostSerializer(
        post, data=request.data, partial=True, context={"request": request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def food_post_delete(request, id):
    """Delete a food post"""
    profile = request.user.userprofile
    post = get_object_or_404(FoodPost, pk=id, user_profile=profile)
    post.delete()
    return Response({"message": "Post deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_food_post_image(request, id):
    """Upload image to a post"""
    profile = request.user.userprofile
    post = get_object_or_404(FoodPost, pk=id, user_profile=profile)

    if "image" not in request.FILES:
        return Response(
            {"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    post.image = request.FILES["image"]
    post.save()
    return Response(
        {"message": "Image uploaded", "image_url": post.image.url},
        status=status.HTTP_200_OK,
    )


# ==================== FOOD POST COMMENTS ====================


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def food_post_comments(request, post_id):
    """List or create comments for a food post"""
    post = get_object_or_404(FoodPost, pk=post_id)

    if request.method == "GET":
        comments = post.comments.all()
        serializer = FoodPostCommentSerializer(
            comments, many=True, context={"request": request}
        )
        return Response(serializer.data)

    elif request.method == "POST":
        profile = request.user.userprofile

        # only the post owner or that member's coach may comment
        if profile.role == "member":
            # member may only comment on their own post
            if post.user_profile != profile:
                return Response(
                    {"error": "Members may only comment on their own posts."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        elif profile.role == "coach":
            # coach must be assigned to the member who created the post
            member = getattr(post.user_profile, "member_profile", None)
            if not member:
                return Response(
                    {"error": "Member profile not found for this post."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            assigned = CoachMemberRelationship.objects.filter(
                coach__user=profile, member=member, status__in=["accepted", "approved"]
            ).exists()
            if not assigned:
                return Response(
                    {"error": "You are not the assigned coach for this member."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        else:
            return Response(
                {"error": "Only members or coaches may comment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Both member and coach can comment
        serializer = FoodPostCommentSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(food_post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def food_post_comment_detail(request, post_id, comment_id):
    """Update or delete a specific comment"""
    comment = get_object_or_404(FoodPostComment, pk=comment_id, food_post_id=post_id)
    profile = request.user.userprofile

    # Only the comment author (coach) can update/delete
    if comment.author != profile:
        return Response(
            {"error": "You can only modify your own comments"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "PUT":
        serializer = FoodPostCommentSerializer(
            comment, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        comment.delete()
        return Response(
            {"message": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def uncommented_food_posts(request):
    """Get food posts that need coach feedback (no comments yet)"""
    profile = request.user.userprofile

    if profile.role != "coach":
        return Response(
            {"error": "Only coaches can access this endpoint"},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Get all food posts where this coach is assigned and has no comments
    uncommented_posts = (
        FoodPost.objects.filter(coach=profile, comments__isnull=True)
        .select_related("user_profile__user")
        .order_by("-created_at")
    )

    # Serialize the posts
    data = []
    for post in uncommented_posts:
        data.append(
            {
                "id": post.id,
                "title": post.title,
                "member_name": post.user_profile.user.username,
                "member_id": getattr(
                    post.user_profile.member_profile, "member_id", "N/A"
                ),
                "created_at": post.created_at,
                "image": post.image.url if post.image else None,
            }
        )

    return Response({"count": len(data), "posts": data}, status=status.HTTP_200_OK)
