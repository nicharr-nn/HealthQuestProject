import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from users.models import UserProfile, WorkoutAssignment, WorkoutProgram

@pytest.mark.django_db
def test_complete_workout_awards_xp():
    user = User.objects.create_user(username="testuser", password="testpass")
    profile = user.userprofile

    program = WorkoutProgram.objects.create(
        coach_id=1,
        title="Beginner Program",
        description="Test Program",
        video_links="",
        level_access="All",
        difficulty_level="Easy",
        is_public=True,
        duration=30,
    )

    assignment = WorkoutAssignment.objects.create(
        user_profile=profile,
        program=program,
    )

    client = APIClient()
    client.login(username="testuser", password="testpass")

    url = f"/api/workouts/{assignment.id}/complete/"
    response = client.post(url)

    assert response.status_code == 201
    data = response.json()
    assert "completion" in data
    assert "xp_earned" in data["completion"]
    assert data["completion"]["xp_earned"] == 50
