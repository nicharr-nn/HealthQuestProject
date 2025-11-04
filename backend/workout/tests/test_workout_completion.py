from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from workout.models import WorkoutProgram, WorkoutDay, WorkoutDayCompletion

User = get_user_model()

class WorkoutDayCompletionTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create user and normal profile
        self.user = User.objects.create_user(
            username="normal_user", password="pass123", email="normal@example.com"
        )
        self.profile = self.user.userprofile
        self.profile.role = "normal"
        self.profile.save()

        # Create a dummy coach (required for WorkoutProgram)
        self.coach_user = User.objects.create_user(
            username="coach", password="coachpass"
        )
        self.coach_profile = self.coach_user.userprofile
        self.coach_profile.role = "coach"
        self.coach_profile.save()

        # Create WorkoutProgram and WorkoutDay
        self.program = WorkoutProgram.objects.create(
            coach=self.coach_profile,
            title="Test Program",
            description="Program for testing XP gain",
            difficulty_level="medium",
            duration=30,
            is_public=True,
        )
        self.workout_day = WorkoutDay.objects.create(
            program=self.program,
            day_number=1,
            title="Day 1 - Test Workout",
            duration=45,
        )

        self.program.days.add(self.workout_day)
        self.program.save()
        self.workout_day.save()

        # Log in as normal user
        self.client.force_login(self.user)

    def test_complete_workout_day_awards_xp(self):
        """Ensure that when a normal user completes a workout day, XP increases."""

        # Get current XP (should exist or create default)
        before_xp = self.profile.get_current_level().xp

        # Send POST request to complete workout day
        url = f"/api/workout/day/{self.workout_day.id}/complete/"
        resp = self.client.post(url, {}, content_type="application/json")

        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        xp_awarded = data.get("xp_awarded", 0)
        self.assertGreater(xp_awarded, 0, "Expected XP to be awarded")

        after_xp = self.profile.get_current_level().xp
        self.assertGreater(
            after_xp,
            before_xp,
            "User XP should increase after completing a workout day",
        )

        # Assertions
        self.assertGreater(xp_awarded, 0, "Expected XP to be awarded by the API")
        self.assertGreater(
            after_xp,
            before_xp,
            "Expected profile XP to increase after workout completion",
        )
        self.assertTrue(
            WorkoutDayCompletion.objects.filter(
                user_profile=self.profile, workout_day=self.workout_day
            ).exists(),
            "WorkoutDayCompletion record should exist after completion",
        )


# in backend : python manage.py test workout
