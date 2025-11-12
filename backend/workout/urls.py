from django.urls import path

from . import views

urlpatterns = [
    path("programs/", views.workout_programs, name="workout-programs"),
    path(
        "programs/create/",
        views.create_workout_programs,
        name="create-workout-programs",
    ),
    path(
        "programs/<int:id>/",
        views.workout_program_detail,
        name="workout-program-detail",
    ),
    path(
        "programs/<int:id>/update/",
        views.update_workout_program,
        name="update-workout-program",
    ),
    path(
        "programs/<int:id>/delete/",
        views.delete_workout_program,
        name="delete-workout-program",
    ),
    path("analytics/", views.user_analytics, name="user-analytics"),
    path(
        "analytics/weekly-activity/",
        views.user_weekly_activity,
        name="weekly-activity",
    ),
    path(
        "day/<int:id>/videos/",
        views.workout_day_videos,
        name="workout-day-videos",
    ),
    path(
        "day/<int:id>/complete/",
        views.complete_workout_day,
        name="complete-workout-day",
    ),
    path(
        "day/<int:id>/complete-status/",
        views.check_workout_day_completion,
        name="check-workout-day-completion",
    ),
    path("progress/<int:id>/", views.workout_progress, name="workout-progress"),
    # Workout Assignment URLs
    path(
        "assignment-update/<int:id>/",
        views.workout_assignment_update,
        name="workout-assignment-update",
    ),
    path(
        "assignment-detail/<int:id>/",
        views.workout_assignment_detail,
        name="workout-assignment-detail",
    ),
    path(
        "assignments/",
        views.list_my_assignments,
        name="list-my-assignments",
    ),
    path("assignment-manage/<int:program_id>", views.manage_workout_assignment, name="manage-assignment"),
    path("assignment-delete/<int:program_id>", views.delete_workout_assignment, name="delete-assignment"),
]
