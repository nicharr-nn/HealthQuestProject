from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from users.models import UserProfile, WorkoutAssignment, WorkoutProgram 

User = get_user_model()

class WorkoutDayCompletionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.profile = getattr(self.user, "userprofile", None) or UserProfile.objects.create(user=self.user)
        self.program = WorkoutProgram.objects.create(name="Test Program")
        self.assignment = WorkoutAssignment.objects.create(user=self.user, program=self.program)
        self.client.force_authenticate(user=self.user)

    def test_complete_workout_awards_xp(self):
        resp = self.client.post("/api/workout/complete/", {"assignment_id": self.assignment.id}, format="json")
        self.assertIn(resp.status_code, (200, 201))
        self.profile.refresh_from_db()
        # Replace 'xp' with the actual field that stores experience points
        self.assertTrue(getattr(self.profile, "xp", 0) > 0)