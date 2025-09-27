from django.urls import path
from . import views


urlpatterns = [
    path("user-info/", views.user_info, name="user-info"),
    path("select-role/", views.set_role, name="select-role"),
    path("select-goal/", views.set_goal, name="select-goal"),
    path("update-profile/", views.update_profile, name="update-profile"),
    path("upload-photo/", views.upload_photo, name="upload-photo"),
    path("users/<int:id>/", views.get_user_by_id, name="get-user-by-id"),
    path("users/<int:id>/update/", views.update_user_by_id, name="update-user-by-id"),
    path("users/<int:id>/delete/", views.delete_user_by_id, name="delete-user-by-id"),
    path("workout-programs/", views.workout_programs, name="workout-programs"),
    path("workout-assignments/<int:id>/", views.workout_assignment_detail, name="workout-assignment-detail"),
]
