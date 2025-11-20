from django.urls import reverse
from rest_framework import status
from workout.models import WorkoutProgram
from .test_admin import AdminTestBase


class AdminWorkoutTests(AdminTestBase):
    """Tests for admin workout management actions."""

    def setUp(self):
        """Set up a workout program for testing."""
        super().setUp()
        self.workout_program = WorkoutProgram.objects.create(
            coach=self.coach_profile,
            title="Test Program",
            description="Program for testing",
            category="full_body",
            difficulty_level="easy",
            duration=7,
            is_public=True,
        )

    def test_admin_can_delete_workout_program(self):
        """Test that an admin can delete a workout program."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("delete_workout", kwargs={"id": self.workout_program.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(WorkoutProgram.DoesNotExist):
            WorkoutProgram.objects.get(pk=self.workout_program.pk)

    def test_non_admin_cannot_delete_workout_program(self):
        """Test that non-admin users cannot delete a workout program."""
        self.client.force_authenticate(user=self.member_user)
        url = reverse("delete_workout", kwargs={"id": self.workout_program.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            WorkoutProgram.objects.filter(pk=self.workout_program.pk).exists()
        )

    def test_delete_nonexistent_workout(self):
        """Test deleting a nonexistent workout program returns 404."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("delete_workout", kwargs={"id": 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_non_admin_cannot_delete_workout(self):
        """Test that non-admin users cannot delete a workout program."""
        self.client.force_authenticate(user=self.member_user)
        url = reverse("delete_workout", kwargs={"id": self.workout_program.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            WorkoutProgram.objects.filter(pk=self.workout_program.pk).exists()
        )
