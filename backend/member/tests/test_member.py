from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from coach.models import Coach
from member.models import Member, CoachMemberRelationship


class MemberModelTests(TestCase):
    """Tests for Member model basic functionality"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@example.com"
        )
        self.profile = self.user.userprofile
        self.profile.role = "member"
        self.profile.save()

    def test_member_creation(self):
        """Test creating a member instance"""
        member = Member.objects.create(
            user=self.profile,
            member_id="M-00000",
            experience_level="intermediate",
            program_name="Test Program",
            message="Test message",
            status="approved",
        )

        self.assertEqual(member.member_id, "M-00000")
        self.assertEqual(member.experience_level, "intermediate")
        self.assertEqual(member.program_name, "Test Program")
        self.assertEqual(member.status, "approved")
        self.assertEqual(str(member), f"{self.user.username} (M-00000 - approved)")

    def test_member_experience_level_choices(self):
        """Test experience level choices are valid"""
        member = Member.objects.create(user=self.profile, member_id="M-00001")

        valid_levels = ["beginner", "intermediate", "advanced"]
        for level in valid_levels:
            member.experience_level = level
            member.save()
            member.refresh_from_db()
            self.assertEqual(member.experience_level, level)

    def test_member_status_choices(self):
        """Test status choices are valid"""
        member = Member.objects.create(user=self.profile, member_id="M-00002")

        valid_statuses = ["pending", "approved", "rejected"]
        for status_choice in valid_statuses:
            member.status = status_choice
            member.save()
            member.refresh_from_db()
            self.assertEqual(member.status, status_choice)


class MemberAPITests(TestCase):
    """Tests for Member API endpoints"""

    def setUp(self):
        self.client = APIClient()

        # Create member user
        self.member_user = User.objects.create_user(
            username="member", password="testpass123"
        )
        self.member_profile = self.member_user.userprofile
        self.member_profile.role = "member"
        self.member_profile.save()

        self.member = Member.objects.create(
            user=self.member_profile, member_id="M-00001"
        )

        # Create coach
        self.coach_user = User.objects.create_user(
            username="coach", password="coachpass"
        )
        self.coach_profile = self.coach_user.userprofile
        self.coach_profile.role = "coach"
        self.coach_profile.save()

        self.coach = Coach.objects.create(
            user=self.coach_profile, public_id="C-00001", status_approval="approved"
        )

        # Create relationship
        self.relationship = CoachMemberRelationship.objects.create(
            coach=self.coach, member=self.member, status="pending"
        )

    def test_apply_as_member_create(self):
        """Test creating a new member application"""
        CoachMemberRelationship.objects.filter(member=self.member).delete()
        self.client.force_login(user=self.member_user)

        url = reverse("apply-as-member")
        data = {
            "experience_level": "advanced",
            "message": "I want to join as a member",
            "coach_code": "C-00001",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that member was created/updated
        self.member.refresh_from_db()
        self.assertEqual(self.member.experience_level, "advanced")
        self.assertEqual(self.member.message, "I want to join as a member")

        # Check that relationship was created
        relationship = CoachMemberRelationship.objects.get(member=self.member)
        self.assertEqual(relationship.coach, self.coach)
        self.assertEqual(relationship.status, "pending")

    def test_apply_as_member_create_failed(self):
        """Test creating a new member application -
        expect 400 due to existing relationship"""
        self.client.force_login(user=self.member_user)

        url = reverse("apply-as-member")
        data = {
            "experience_level": "advanced",
            "message": "I want to join as a member",
            "coach_code": "C-00001",
        }

        response = self.client.post(url, data, format="json")

        # Since there's already a relationship, expect 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already have", response.data["error"])

        # But member should still be updated
        self.member.refresh_from_db()
        self.assertEqual(self.member.experience_level, "advanced")
        self.assertEqual(self.member.message, "I want to join as a member")

    def test_apply_as_member_update(self):
        """Test updating an existing member application"""
        self.client.force_login(user=self.member_user)

        url = reverse("apply-as-member")
        data = {"experience_level": "intermediate", "message": "Updated message"}

        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        member = Member.objects.get(user=self.member_profile)
        self.assertEqual(member.experience_level, "intermediate")
        self.assertEqual(member.message, "Updated message")

    def test_get_member_profile(self):
        """Test retrieving member profile"""
        self.client.force_authenticate(user=self.member_user)

        url = reverse("get-member-profile")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["member_id"], "M-00001")

    def test_manage_member_request_get(self):
        """Test getting member's coach request"""
        self.client.force_authenticate(user=self.member_user)

        url = reverse("manage-member-request")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "pending")

    def test_manage_member_request_delete(self):
        """Test canceling member's coach request"""
        self.client.force_authenticate(user=self.member_user)

        url = reverse("manage-member-request")
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify relationship was deleted
        with self.assertRaises(CoachMemberRelationship.DoesNotExist):
            CoachMemberRelationship.objects.get(member=self.member)
