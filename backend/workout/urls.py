from django.urls import path

from . import views

urlpatterns = [
    path("programs/", views.workout_programs, name="workout-programs"),
    path(
        "programs/<int:id>/",
        views.workout_program_detail,
        name="workout-program-detail",
    ),
    path(
        "assignment/<int:id>/",
        views.workout_assignments,
        name="workout-assignments",
    ),
    path(
        "assignment-update/<int:id>/",
        views.workout_assignments_update,
        name="workout-assignment-update",
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
        "progress/<int:id>/", views.workout_progress, name="workout-progress"
    ),
]
