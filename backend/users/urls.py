from django.urls import path
from . import views


urlpatterns = [
    path("user-info/", views.user_info, name="user-info"),
    path("select-role/", views.set_role, name="select-role"),
    path("select-goal/", views.set_goal, name="select-goal"),
    path("update-profile/", views.update_profile, name="update-profile"),
    path("upload-photo/", views.upload_photo, name="upload-photo"),
    path("coach-portal/", views.coach_portal, name="coach-portal"),
]
