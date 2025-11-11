from django.urls import path
from . import views

urlpatterns = [
    path("admin/coaches/", views.list_coaches_for_admin, name="list_coaches"),
    path(
        "admin/coaches/<int:coach_id>/approve/",
        views.approve_coach,
        name="approve_coach",
    ),
    path(
        "admin/coaches/<int:coach_id>/reject/", views.reject_coach, name="reject_coach"
    ),
]
