from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from workout.models import WorkoutProgram
from coach.models import Coach
from member.models import UserProfile


class WorkoutViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Coach user
        self.coach_user = User.objects.create_user(username="coach", password="pass")
        self.coach_profile = self.coach_user.userprofile
        self.coach_profile.role = "coach"
        self.coach_profile.save()
        self.coach = Coach.objects.create(
            user=self.coach_profile,
            public_id="C-0001",
            status_approval="approved"
        )

        # Workout program
        self.workout = WorkoutProgram.objects.create(
            title="Test Workout",
            description="Some description",
            coach=self.coach.user,
            difficulty_level="easy"
        )

    def test_coach_can_delete_own_workout(self):
        self.client.force_authenticate(user=self.coach_user)
        url = reverse("delete_workout", kwargs={"id": self.workout.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(WorkoutProgram.objects.filter(pk=self.workout.pk).exists())

    def test_non_coach_cannot_delete_workout(self):
        other_user = User.objects.create_user(username="member", password="pass2")
        self.client.force_authenticate(user=other_user)
        url = reverse("delete_workout", kwargs={"id": self.workout.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
