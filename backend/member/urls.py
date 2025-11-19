from django.urls import path
from .views import (
    coach_member_requests,
    coach_member_profile,
    accepted_members,
    coach_remove_member,
    apply_as_member,
    get_member_profile,
    manage_member_request,
    food_posts,
    food_post_update,
    food_post_delete,
    upload_food_post_image,
    food_post_comments,
    food_post_comment_detail,
    uncommented_food_posts,
)

urlpatterns = [
    path("coach-requests/", coach_member_requests, name="coach-member-requests"),
    path(
        "coach-requests/<int:pk>/",
        coach_member_requests,
        name="coach-member-requests-detail",
    ),
    path("accepted/", accepted_members, name="accepted-members"),
    # coach can view member profile
    path("profile/<str:member_id>/", coach_member_profile, name="member-profile"),
    # member specific endpoints
    path("member-apply/", apply_as_member, name="apply-as-member"),
    path("member-profile/", get_member_profile, name="get-member-profile"),
    path("member-request/", manage_member_request, name="manage-member-request"),
    # food post endpoints
    path("food-posts/", food_posts, name="food-posts"),
    path("food-posts/<int:id>/update/", food_post_update, name="food-post-update"),
    path("food-posts/<int:id>/delete/", food_post_delete, name="food-post-delete"),
    path(
        "food-posts/<int:id>/upload-image/",
        upload_food_post_image,
        name="upload-food-post-image",
    ),
    # comment endpoints
    path(
        "food-posts/<int:post_id>/comments/",
        food_post_comments,
        name="food-post-comments",
    ),
    path(
        "food-posts/<int:post_id>/comments/<int:comment_id>/",
        food_post_comment_detail,
        name="food-post-comment-detail",
    ),
    # notification endpoints
    path(
        "food-posts/pending-feedback/",
        uncommented_food_posts,
        name="uncommented-food-posts",
    ),
    # coach can remove an accepted member
    path("<str:member_id>/", coach_remove_member, name="coach-remove-member"),
]
