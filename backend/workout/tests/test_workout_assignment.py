from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from rest_framework import status
from workout.models import (
    WorkoutAssignment,
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
            member=self.member, program=self.program, status="pending"
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
        self.assertEqual(assignment_data["status"], "pending")

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

        url = reverse("assign-program-to-member")
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

        url = reverse("assign-program-to-member")
        data = {
            "program_id": new_program.id,
            # Missing member_id
            "due_date": (timezone.now() + timedelta(days=30)).date().isoformat(),
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Member ID is required", response.data["error"])

    def test_assign_program_to_member_as_member(self):
        """Test member cannot assign programs"""
        url = reverse("assign-program-to-member")
        data = {"program_id": self.program.id}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_assign_duplicate_program(self):
        """Test cannot assign duplicate program to same member"""
        self.client.force_login(self.coach_user)

        url = reverse("assign-program-to-member")
        data = {"program_id": self.program.id, "member_id": self.member.member_id}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("already assigned", response.data["message"].lower())
        self.assertEqual(WorkoutAssignment.objects.count(), 1)  # Still only one

    def test_get_assignment_detail_as_member(self):
        """Test member can get their assignment detail"""
        url = reverse(
            "workout-assignment-detail", kwargs={"id": self.workout_assignment.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.workout_assignment.id)

    def test_get_assignment_detail_as_other_member(self):
        """Test member cannot access other member's assignment"""
        other_member_user = User.objects.create_user(
            username="othermember", password="otherpass"
        )
        other_member_profile = other_member_user.userprofile
        other_member_profile.role = "member"
        other_member_profile.save()

        self.client.force_login(other_member_user)

        url = reverse(
            "workout-assignment-detail", kwargs={"id": self.workout_assignment.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_assignment_status(self):
        """Test member can update assignment status to completed"""
        url = reverse(
            "workout-assignment-update", kwargs={"id": self.workout_assignment.id}
        )
        response = self.client.patch(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.workout_assignment.refresh_from_db()
        self.assertEqual(self.workout_assignment.status, "completed")
        self.assertIsNotNone(self.workout_assignment.completed_date)
        self.assertIn("xp_awarded", response.data)

    def test_assign_program_without_due_date(self):
        """Test assignment works without due date"""
        self.client.force_login(self.coach_user)

        new_program = WorkoutProgram.objects.create(
            coach=self.coach_profile,
            title="Test Program No Due Date",
            description="Test description",
            difficulty_level="easy",
            duration=5,
        )

        url = reverse("assign-program-to-member")
        data = {
            "program_id": new_program.id,
            "member_id": self.member.member_id,
            # No due_date provided
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorkoutAssignment.objects.count(), 2)

        # Check that assignment was created without due date
        new_assignment = WorkoutAssignment.objects.get(
            program=new_program, member=self.member
        )
        self.assertIsNone(new_assignment.due_date)

    def test_assign_program_to_member_nonexistent_member(self):
        """Test assignment fails when member doesn't exist"""
        self.client.force_login(self.coach_user)

        new_program = WorkoutProgram.objects.create(
            coach=self.coach_profile,
            title="Test Program",
            description="Test description",
            difficulty_level="medium",
            duration=7,
        )

        url = reverse("assign-program-to-member")
        data = {
            "program_id": new_program.id,
            "member_id": "M-99999",  # Non-existent member
            "due_date": (timezone.now() + timedelta(days=30)).date().isoformat(),
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Member not found", response.data["error"])

    def test_assign_program_to_member_nonexistent_program(self):
        """Test assignment fails when program doesn't exist"""
        self.client.force_login(self.coach_user)

        url = reverse("assign-program-to-member")
        data = {
            "program_id": 99999,  # Non-existent program
            "member_id": self.member.member_id,
            "due_date": (timezone.now() + timedelta(days=30)).date().isoformat(),
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
