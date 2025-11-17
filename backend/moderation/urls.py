from django.urls import path
from . import views
urlpatterns = [
    path(
        "recipe/<int:recipe_id>/delete/",
        views.delete_recipe,
        name="delete_recipe"),
    path(
        "workout/programs/<int:id>/delete/",
        views.delete_workout,
        name="delete_workout"),
    path("admin/coaches/",
         views.list_coaches_for_admin,
         name="list_coaches"),
    path(
        "admin/coaches/<int:coach_id>/approve/",
        views.approve_coach,
        name="approve_coach"),
    path(
        "admin/coaches/<int:coach_id>/reject/",
        views.reject_coach,
        name="reject_coach"),
    path(
        "admin/coaches/",
        views.list_coaches_for_admin,
        name="admin_list_coaches"),
    path(
        "admin/users/",
        views.list_all_users,
        name="admin_list_users"),
    path(
        "admin/users/<int:user_id>/delete/",
        views.delete_user,
        name="admin_delete_user"),
]
