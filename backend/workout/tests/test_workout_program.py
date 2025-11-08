from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from workout.models import (
    WorkoutProgram,
    WorkoutDay,
    WorkoutDayCompletion,
)
from coach.models import Coach

User = get_user_model()


class WorkoutProgramTests(TestCase):
    """Tests for WorkoutProgram views"""

    def setUp(self):
        self.client = APIClient()

        # Create normal user
        self.normal_user = User.objects.create_user(
            username="normal_user", password="pass123", email="normal@example.com"
        )
        self.normal_profile = self.normal_user.userprofile
        self.normal_profile.role = "normal"
        self.normal_profile.save()

        # Create coach user
        self.coach_user = User.objects.create_user(
            username="coach", password="coachpass", email="coach@example.com"
        )
        self.coach_profile = self.coach_user.userprofile
        self.coach_profile.role = "coach"
        self.coach_profile.save()

        # Create coach model instance
        self.coach = Coach.objects.create(
            user=self.coach_profile, public_id="C-00001", status_approval="approved"
        )

        # Create workout program
        self.program = WorkoutProgram.objects.create(
            coach=self.coach_profile,
            title="Test Program",
            description="Program for testing",
            difficulty_level="easy",
            duration=1,
            is_public=True,
            category="cardio",
        )

        # Create workout days
        self.workout_day_1 = WorkoutDay.objects.create(
            program=self.program,
            day_number=1,
            title="Day 1 - Test Workout",
            duration=30,
        )

        # Default authentication as normal user
        self.client.force_login(self.normal_user)

    def test_get_workout_programs_as_normal_user(self):
        """Test normal user can retrieve workout programs"""
        url = reverse("workout-programs")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        if response.data:  # If there are programs
            program_data = response.data[0]
            self.assertIn("id", program_data)
            self.assertIn("title", program_data)
            self.assertIn("description", program_data)

    def test_create_workout_program_as_coach(self):
        """Test coach can create workout program"""
        self.client.force_login(self.coach_user)

        url = reverse("workout-programs")
        data = {
            "title": "New Program",
            "description": "New program description",
            "difficulty_level": "easy",
            "duration": 1,
            "is_public": True,
            "category": "cardio",
            "coach": self.coach_profile.id,
            "days": [
                {
                    "id": 1,
                    "day_number": 1,
                    "title": "lower",
                    "video_links": ["https://youtube.com/watch?v=example"],
                    "duration": 30,
                },
            ],
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorkoutProgram.objects.count(), 2)
        self.assertEqual(response.data["title"], "New Program")

    def test_create_workout_program_as_normal_user(self):
        """Test normal user cannot create workout program"""
        url = reverse("workout-programs")
        data = {
            "title": "Normal user Program",
            "description": "Should not work",
            "difficulty_level": "easy",
            "duration": 1,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(WorkoutProgram.objects.count(), 1)

    def test_get_workout_program_detail(self):
        """Test retrieving specific workout program"""
        url = reverse("workout-program-detail", kwargs={"id": self.program.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.program.title)
        self.assertEqual(response.data["id"], self.program.id)

    def test_update_workout_program_as_coach(self):
        """Test coach can update their workout program"""
        self.client.force_login(self.coach_user)

        url = reverse("workout-program-detail", kwargs={"id": self.program.id})
        data = {
            "title": "Updated Program Title",
            "description": "Updated description",
            "difficulty_level": "medium",
            "duration": 3,
        }
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.program.refresh_from_db()
        self.assertEqual(self.program.title, "Updated Program Title")

    def test_update_workout_program_as_normal(self):
        """Test normal cannot update workout program"""
        url = reverse("workout-program-detail", kwargs={"id": self.program.id})
        data = {"title": "Unauthorized Update"}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_workout_program_as_coach(self):
        """Test coach can delete their workout program"""
        self.client.force_login(self.coach_user)

        url = reverse("workout-program-detail", kwargs={"id": self.program.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WorkoutProgram.objects.count(), 0)

    def test_delete_workout_program_as_normal(self):
        """Test normal cannot delete workout program"""
        url = reverse("workout-program-detail", kwargs={"id": self.program.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(WorkoutProgram.objects.count(), 1)


class WorkoutDayCompletionTests(WorkoutProgramTests):
    """Tests for workout day completion functionality"""

    def test_complete_workout_day(self):
        """Test normal can complete a workout day"""
        url = reverse("complete-workout-day", kwargs={"id": self.workout_day_1.id})
        response = self.client.post(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("xp_awarded", response.data)
        self.assertIn("goal_achieved", response.data)
        self.assertTrue(response.data["completed"])
        self.assertEqual(response.data["total_xp"], 530)

        # Check completion was created
        completion = WorkoutDayCompletion.objects.filter(
            user_profile=self.normal_profile, workout_day=self.workout_day_1
        ).first()
        self.assertIsNotNone(completion)
        self.assertEqual(completion.xp_earned, response.data["xp_awarded"])

    def test_complete_already_completed_workout_day(self):
        """Test completing already completed workout day"""
        # First completion
        url = reverse("complete-workout-day", kwargs={"id": self.workout_day_1.id})
        first_response = self.client.post(url, format="json")
        self.assertEqual(first_response.status_code, status.HTTP_200_OK)

        # Store XP after first completion
        xp_after_first = first_response.data["total_xp"]

        url = reverse("complete-workout-day", kwargs={"id": self.workout_day_1.id})
        # try to make complete again
        response = self.client.post(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["completed"])
        self.assertEqual(response.data["total_xp"], xp_after_first)
        # No new XP for already-completed day
        self.assertEqual(response.data["xp_awarded"], 0)
        self.assertEqual(response.data["current_level"], "Bronze")
        self.assertEqual(response.data["goal_achieved"], False)

        # Should still only have one completion
        completions = WorkoutDayCompletion.objects.filter(
            user_profile=self.normal_profile, workout_day=self.workout_day_1
        )
        self.assertEqual(completions.count(), 1)

    def test_check_completion_status(self):
        """Test checking completion status of workout day"""
        url_get = reverse(
            "check-workout-day-completion", kwargs={"id": self.workout_day_1.id}
        )
        url_post = reverse("complete-workout-day", kwargs={"id": self.workout_day_1.id})

        # Check before completion
        response = self.client.get(url_get)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["completed"])

        # Complete the workout
        self.client.post(url_post, format="json")

        # Check after completion
        response = self.client.get(url_get)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["completed"])
        self.assertIn("xp_earned", response.data)


class WorkoutProgressTests(WorkoutProgramTests):
    """Tests for workout progress tracking"""

    def test_workout_progress_no_completions(self):
        """Test progress for program with no completions"""
        url = reverse("workout-progress", kwargs={"id": self.program.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["program_id"], self.program.id)
        self.assertEqual(response.data["completed_days"], 0)
        self.assertEqual(response.data["completion_percentage"], 0)
        self.assertEqual(response.data["xp_earned"], 0)
        self.assertEqual(response.data["total_days"], 1)

    def test_workout_progress_with_completions(self):
        """Test progress for program with some completions"""
        WorkoutDayCompletion.objects.create(
            user_profile=self.normal_profile,
            workout_day=self.workout_day_1,
            xp_earned=150,
        )

        url = reverse("workout-progress", kwargs={"id": self.program.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["completed_days"], 1)
        self.assertEqual(response.data["completion_percentage"], 100)
        self.assertEqual(response.data["xp_earned"], 150)
        self.assertEqual(response.data["completed_day_numbers"], [1])

    def test_workout_progress_nonexistent_program(self):
        """Test progress for non-existent program"""
        url = reverse("workout-progress", kwargs={"id": 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class WorkoutDayVideoTests(WorkoutProgramTests):
    """Tests for workout day video functionality"""

    def test_get_workout_day_videos(self):
        """Test retrieving workout day videos"""
        # Add some video links
        self.workout_day_1.video_links = [
            "https://youtube.com/watch?v=test1",
            "https://youtube.com/watch?v=test2",
        ]
        self.workout_day_1.save()

        url = reverse("workout-day-videos", kwargs={"id": self.workout_day_1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["video_links"]), 2)

    def test_add_workout_day_video_as_coach(self):
        """Test coach can add video to workout day"""
        self.client.force_login(self.coach_user)

        url = reverse("workout-day-videos", kwargs={"id": self.workout_day_1.id})
        data = {"link": "https://youtube.com/watch?v=newvideo"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.workout_day_1.refresh_from_db()
        self.assertIn(
            "https://youtube.com/watch?v=newvideo", self.workout_day_1.video_links
        )

    def test_add_workout_day_video_as_normal(self):
        """Test normal cannot add videos"""
        url = reverse("workout-day-videos", kwargs={"id": self.workout_day_1.id})
        data = {"link": "https://youtube.com/watch?v=normalvideo"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_workout_day_video_missing_link(self):
        """Test adding video without link fails"""
        self.client.force_login(self.coach_user)

        url = reverse("workout-day-videos", kwargs={"id": self.workout_day_1.id})
        data = {}  # Missing link
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
