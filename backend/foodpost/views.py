from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import FoodPost

# from coachmember.models import CoachMemberRealtionship


# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
# def food_posts(request):
#     """List or create food posts"""
#     if request.method == "GET":
#         posts = FoodPost.objects.all().select_related("user_profile", "coach")
#         data = [
#             {
#                 "id": p.id,
#                 "title": p.title,
#                 "content": p.content,
#                 "image": p.image.url if p.image else None,
#                 "author": p.user_profile.user.username,
#                 "coach": p.coach.user.username if p.coach else None,
#                 "created_at": p.created_at,
#             }
#             for p in posts
#         ]
#         return Response(data)

#     elif request.method == "POST":
#         pass
#         profile = request.user.userprofile

#         # Only members can create posts
#         if profile.role != "member":
#             return Response(
#                 {"detail": "Only members can create food posts."},
#                 status=403,
#             )

#         # Get active coach-member relationship
#         coach_relation = (
#             CoachMemberRealtionship.objects.filter(user=profile, status="active")
#             .select_related("coach")
#             .first()
#         )

#         if not coach_relation:
#             return Response(
#                 {"detail": "You are not currently assigned to a coach."},
#                 status=400,
#             )

#         coach_profile = coach_relation.coach.userprofile

#         # Create post with coach attached
#         post = FoodPost.objects.create(
#             user_profile=profile,
#             coach=coach_profile,
#             title=request.data.get("title"),
#             content=request.data.get("content"),
#         )

#         return Response(
#             {
#                 "message": "Post created successfully.",
#                 "post_id": post.id,
#                 "coach": coach_profile.user.username,
#             }
#         )


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def food_post_update(request, id):
    """update to a food post"""
    profile = request.user.userprofile
    post = get_object_or_404(FoodPost, pk=id, user_profile=profile)

    if request.method in ["PUT", "PATCH"]:
        post.title = request.data.get("title", post.title)
        post.content = request.data.get("content", post.content)
        post.save()
        return Response({"message": "Post updated"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_food_post_image(request, id):
    """Upload an image for a food post"""
    profile = request.user.userprofile
    post = get_object_or_404(FoodPost, pk=id, user_profile=profile)

    if "image" not in request.FILES:
        return Response({"error": "No image provided"}, status=400)

    post.image = request.FILES["image"]
    post.save()
    return Response(
        {
            "message": "Image uploaded",
            "image_url": post.image.url if post.image else None,
        },
        status=200,
    )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def food_post_delete(request, id):
    """Delete a food post"""
    profile = request.user.userprofile
    post = get_object_or_404(FoodPost, pk=id, user_profile=profile)
    post.delete()
    return Response({"message": "Post deleted"}, status=204)
