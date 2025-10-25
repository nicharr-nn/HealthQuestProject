from django.urls import path
from .views import (
    coach_member_requests,
    accepted_members,
    apply_as_member,
    get_member_profile,
    manage_member_request,
    food_posts,
    food_post_update,
    food_post_delete,
    upload_food_post_image,
)

urlpatterns = [
    path("coach-requests/", coach_member_requests, name="coach-member-requests"),
    path(
        "coach-requests/<int:pk>/",
        coach_member_requests,
        name="coach-member-requests-detail",
    ),
    path("accepted/", accepted_members, name="accepted-members"),
    # member specific endpoints
    path("member-apply/", apply_as_member, name="apply_as_member"),
    path("member-profile/", get_member_profile, name="get_member_profile"),
    path("member-request/manage/", manage_member_request, name="manage_member_request"),
    # food post endpoints
    path("food-posts/", food_posts, name="food-posts"),
    path("food-posts/<int:id>/update/", food_post_update, name="food-post-update"),
    path("food-posts/<int:id>/delete/", food_post_delete, name="food-post-delete"),
    path(
        "food-posts/<int:id>/upload-image/",
        upload_food_post_image,
        name="upload-food-post-image",
    ),
]
