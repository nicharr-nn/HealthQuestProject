from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from rest_framework import status
from workout.models import (
    WorkoutAssignment,
    WorkoutDayCompletion,
    WorkoutProgram,
    WorkoutDay,
)
from member.models import Member, CoachMemberRelationship
from coach.models import Coach

User = get_user_model()


class WorkoutAssignmentTests(TestCase):
    """Tests for workout assignment functionality"""

    def setUp(self):
        self.client = APIClient()

        # Create member user
        self.member_user = User.objects.create_user(
            username="member", password="pass123", email="member@example.com"
        )
        self.member_profile = self.member_user.userprofile
        self.member_profile.role = "member"
        self.member_profile.save()

        # Create member model instance
        self.member = Member.objects.create(
            user=self.member_profile, member_id="M-00001", status="approved"
        )

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

        # Create coach-member relationship
        CoachMemberRelationship.objects.create(
            coach=self.coach, member=self.member, status="accepted"
        )

        # Create workout program
        self.program = WorkoutProgram.objects.create(
            coach=self.coach_profile,
            title="Test Program",
            description="Program for testing",
            difficulty_level="medium",
            duration=2,
            is_public=True,
            category="strength_training",
        )

        # Create workout days
        self.workout_day_1 = WorkoutDay.objects.create(
            program=self.program,
            day_number=1,
            title="Day 1 - Test Workout",
            duration=45,
        )
        self.workout_day_2 = WorkoutDay.objects.create(
            program=self.program,
            day_number=2,
            title="Day 2 - Test Workout",
            duration=30,
        )

        # Create workout assignment
        self.workout_assignment = WorkoutAssignment.objects.create(
            member=self.member, program=self.program, status="assigned"
        )

        # Default authentication as member
        self.client.force_login(self.member_user)

    def test_list_my_assignments_as_member(self):
        """Test member can list their assignments"""
        url = reverse("list-my-assignments")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        assignment_data = response.data[0]
        self.assertEqual(assignment_data["program"]["title"], self.program.title)
        self.assertEqual(assignment_data["status"], "assigned")

    def test_list_my_assignments_as_coach(self):
        """Test coach can list their assigned programs"""
        self.client.force_login(self.coach_user)

        url = reverse("list-my-assignments")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_assign_program_to_member_as_coach(self):
        """Test coach can assign program to member"""
        self.client.force_login(self.coach_user)

        # Create another program to assign
        new_program = WorkoutProgram.objects.create(
            coach=self.coach_profile,
            title="New Assignment Program",
            description="For assignment testing",
            difficulty_level="hard",
            duration=14,
            is_public=False,
        )

        url = reverse("manage-assignment", kwargs={"program_id": new_program.id})
        data = {
            "program_id": new_program.id,
            "member_id": self.member.member_id,
            "due_date": (timezone.now() + timedelta(days=30)).date().isoformat(),
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorkoutAssignment.objects.count(), 2)
        self.assertIn("assignment", response.data)

    def test_assign_program_to_member_missing_member_id(self):
        """Test assignment fails when member_id is missing"""
        self.client.force_login(self.coach_user)

        new_program = WorkoutProgram.objects.create(
            coach=self.coach_profile,
            title="Test Program",
            description="Test description",
            difficulty_level="medium",
            duration=7,
        )

        url = reverse("manage-assignment", kwargs={"program_id": new_program.id})
        data = {
            "program_id": new_program.id,
            # Missing member_id
            "due_date": (timezone.now() + timedelta(days=30)).date().isoformat(),
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("member_id is required", response.data["error"])

    def test_assign_program_to_member_as_member(self):
        """Test member cannot assign programs"""
        url = reverse("manage-assignment", kwargs={"program_id": self.program.id})
        data = {"program_id": self.program.id}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_assignment_status(self):
        """Test member can update assignment status to in_progress"""
        WorkoutDayCompletion.objects.create(
            user_profile=self.member_profile,
            workout_day=self.workout_day_1,
            xp_earned=50,
        )

        url = reverse("update_assignment", kwargs={"id": self.workout_assignment.id})
        response = self.client.patch(url, {"action": "start"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.workout_assignment.refresh_from_db()
        self.assertEqual(self.workout_assignment.status, "in_progress")
        self.assertEqual(response.data["message"], "Assignment is already in_progress.")

    def test_start_assignment(self):
        """Test member can start an assignment"""
        self.workout_assignment.status = "assigned"
        self.workout_assignment.save()
        url = reverse("update_assignment", kwargs={"id": self.workout_assignment.id})
        response = self.client.patch(url, {"action": "start"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.workout_assignment.refresh_from_db()
        self.assertEqual(self.workout_assignment.status, "in_progress")
        self.assertEqual(response.data["status"], "in_progress")

    def test_complete_assignment_without_finishing_workouts(self):
        """Test cannot complete assignment without finishing all workout days"""
        # Only complete one workout day
        self.workout_assignment.status = "assigned"
        self.workout_assignment.save()
        WorkoutDayCompletion.objects.create(
            user_profile=self.member_profile,
            workout_day=self.workout_day_1,
            xp_earned=50,
        )

        url = reverse("update_assignment", kwargs={"id": self.workout_assignment.id})
        response = self.client.patch(url, {"action": "complete"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.workout_assignment.refresh_from_db()
        self.assertIn(self.workout_assignment.status, ["assigned", "in_progress"])

    def test_delete_assignment_as_coach(self):
        """Test coach can delete an assignment"""
        self.client.force_login(self.coach_user)

        url = reverse(
            "delete-assignment", kwargs={"program_id": self.program.id}
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        self.assertFalse(
            WorkoutAssignment.objects.filter(
                id=self.workout_assignment.id
            ).exists()
        )
        
        self.assertTrue(
            WorkoutProgram.objects.filter(id=self.program.id).exists()
        )
