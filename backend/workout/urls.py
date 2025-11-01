from django.urls import path

from . import views

urlpatterns = [
    path("programs/", views.workout_programs, name="workout-programs"),
    path(
        "programs/<int:id>/",
        views.workout_program_detail,
        name="workout-program-detail",
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
    path("progress/<int:id>/", views.workout_progress, name="workout-progress"),

    # Workout Assignment URLs
    path(
        "assign/<int:member_id>/",
        views.assign_program_to_member,
        name="assign_program_to_member",
    ),
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
]
