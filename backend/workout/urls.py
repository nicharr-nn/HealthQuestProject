from django.urls import path
from . import views

urlpatterns = [
    path("programs/", views.workout_programs, name="workout-programs"),
    path("assignment/<int:id>/", views.workout_assignments, name="workout-assignments"),
    path("assignment-update/<int:id>/", views.workout_assignments_update, name="workout-assignment-update"),
    path('analytics/', views.user_analytics, name='user-analytics'),
]