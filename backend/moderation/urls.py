from django.urls import path
from . import views

urlpatterns = [
    # Admin Coach Management
    path("admin/coaches/",
         views.list_coaches_for_admin, name="admin_list_coaches"),
    path("admin/coaches/<int:coach_id>/approve/",
         views.approve_coach, name="admin_approve_coach"),
    path("admin/coaches/<int:coach_id>/reject/",
         views.reject_coach, name="admin_reject_coach"),

    # Admin User Management
    path("admin/users/", 
         views.list_all_users, name="admin_list_users"),
    path("admin/users/<int:user_id>/delete/",
         views.delete_user, name="admin_delete_user"),
]
