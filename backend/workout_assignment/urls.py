from django.urls import path

from . import views

urlpatterns = [
    path(
        "assign/<int:id>/",
        views.assign_program_to_member,
        name="assign_program_to_member",
    ),
    path(
        "assignment-update/<int:id>/",
        views.workout_assignment_update,
        name="workout-assignment-update",
    ),
]
