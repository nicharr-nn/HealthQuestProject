from django.urls import path
from . import views


urlpatterns = [
    path("user-info/", views.user_info, name="user-info"),
    path("select-role/", views.set_role, name="select-role"),
    path("select-goal/", views.set_goal, name="select-goal"),
    path("update-profile/", views.update_profile, name="update-profile"),
    path("upload-photo/", views.upload_photo, name="upload-photo"),
    path("users/<int:id>/", views.user_detail, name="user_detail"),

    # workout program and assignment endpoints
    path("programs/", views.workout_programs, name="workout-programs"),
    path("assignments/", views.workout_assignments, name="workout-assignments"),
    path("assignments/<int:id>/", views.workout_assignments_update, name="workout-assignment-detail"),
    
    # Levels & Achievements
    path("achievements/", views.achievements, name="all-achievements"),
    path("user/achievements/", views.user_achievements, name="user-achievements"),

    # Food post
    path("food-posts/", views.food_posts, name="food-posts"),
#    path("food-posts/<int:id>/comments", views.food_post_comment, name="food-post-comment"),
    path("food-posts/<int:id>", views.food_post_update, name="food-post-update"),
    
]
