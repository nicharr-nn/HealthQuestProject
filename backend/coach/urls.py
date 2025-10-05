from django.urls import path

from . import views

urlpatterns = [
    path("status/", views.coach_status, name="coach_status"),
    path("upload-cert/", views.upload_certification, name="upload_certification"),
    path("edit-profile/", views.edit_coach_profile, name="edit_coach_profile"),
]
