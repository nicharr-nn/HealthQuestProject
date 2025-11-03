from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from workout.models import (
    WorkoutAssignment,
    WorkoutProgram,
    WorkoutDay,
    WorkoutDayCompletion,
    WorkoutAssignment,
)

User = get_user_model()


class WorkoutAssignmentTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create user and member profile
        self.member = User.objects.create_user(
            username="member", password="pass123", email="member@example.com"
        )

        self.profile = self.member.userprofile
        self.profile.role = "member"
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
        self.workout_assignment = WorkoutAssignment.objects.create()

        self.program.days.add(self.workout_day)
        self.program.save()
        self.workout_day.save()

        # Log in as member
        self.client.force_login(self.member)
