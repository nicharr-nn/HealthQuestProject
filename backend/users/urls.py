from django.urls import path

from . import views

urlpatterns = [
    path("user-info/", views.user_info, name="user-info"),
    path("select-role/", views.set_role, name="select-role"),
    path("select-goal/", views.set_goal, name="select-goal"),
    path("update-profile/", views.update_profile, name="update-profile"),
    path("upload-photo/", views.upload_photo, name="upload-photo"),
    path("user/<int:id>/", views.user_detail, name="user_detail"),
    path("users/", views.all_users, name="all-users"),
    # Levels & Achievements
    path("achievements/", views.achievements, name="all-achievements"),
    path("user/achievements/", views.user_achievements, name="user-achievements"),
]
