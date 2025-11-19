from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from coach.models import Coach
from member.models import Member, CoachMemberRelationship
from django.db import IntegrityError


class CoachMemberRelationshipTests(TestCase):
    """Tests for CoachMemberRelationship model"""

    def setUp(self):
        # Create member
        self.member_user = User.objects.create_user(
            username="member", password="memberpass"
        )
        self.member_profile = self.member_user.userprofile
        self.member_profile.role = "member"
        self.member_profile.save()

        self.member = Member.objects.create(user=self.member_profile, member_id="M-001")

        # Create coach
        self.coach_user = User.objects.create_user(
            username="coach", password="coachpass"
        )
        self.coach_profile = self.coach_user.userprofile
        self.coach_profile.role = "coach"
        self.coach_profile.save()

        self.coach = Coach.objects.create(
            user=self.coach_profile, public_id="C-001", status_approval="approved"
        )

    def test_relationship_creation(self):
        """Test creating a coach-member relationship"""
        relationship = CoachMemberRelationship.objects.create(
            coach=self.coach, member=self.member, status="accepted"
        )

        self.assertEqual(relationship.coach, self.coach)
        self.assertEqual(relationship.member, self.member)
        self.assertEqual(relationship.status, "accepted")
        self.assertEqual(str(relationship), f"{self.coach} → {self.member} (accepted)")

    def test_relationship_status_choices(self):
        """Test relationship status choices"""
        relationship = CoachMemberRelationship.objects.create(
            coach=self.coach, member=self.member
        )

        valid_statuses = ["pending", "accepted", "rejected"]
        for status_choice in valid_statuses:
            relationship.status = status_choice
            relationship.save()
            relationship.refresh_from_db()
            self.assertEqual(relationship.status, status_choice)

    def test_unique_member_relationship(self):
        """Test that a member can only have one relationship"""
        CoachMemberRelationship.objects.create(coach=self.coach, member=self.member)

        other_coach_user = User.objects.create_user(
            username="coach2", password="coach2pass"
        )
        other_coach_profile = other_coach_user.userprofile
        other_coach_profile.role = "coach"
        other_coach_profile.save()
        another_coach = Coach.objects.create(
            user=other_coach_profile, public_id="C-00002", status_approval="approved"
        )

        # creating a second relationship for the same member should raise IntegrityError
        with self.assertRaises(IntegrityError):
            CoachMemberRelationship.objects.create(
                coach=another_coach, member=self.member
            )


class CoachMemberRelationshipAPITests(TestCase):
    """Tests for coach-member relationship API endpoints"""

    def setUp(self):
        self.client = APIClient()

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

        # Create member
        self.member_user = User.objects.create_user(
            username="member", password="memberpass"
        )
        self.member_profile = self.member_user.userprofile
        self.member_profile.role = "member"
        self.member_profile.save()

        self.member = Member.objects.create(
            user=self.member_profile, member_id="M-00001"
        )

        # Create relationship
        self.relationship = CoachMemberRelationship.objects.create(
            coach=self.coach, member=self.member, status="pending"
        )

    def test_coach_get_relationships(self):
        """Test coach retrieving member relationships"""
        self.client.force_authenticate(user=self.coach_user)

        url = reverse("coach-member-requests")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["status"], "pending")

    def test_coach_update_relationship_status(self):
        """Test coach updating relationship status"""
        self.client.force_authenticate(user=self.coach_user)

        url = reverse(
            "coach-member-requests-detail", kwargs={"pk": self.relationship.pk}
        )
        data = {"status": "accepted"}

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh from database
        self.relationship.refresh_from_db()
        self.member.refresh_from_db()

        self.assertEqual(self.relationship.status, "accepted")
        self.assertEqual(self.member.status, "approved")

    def test_coach_get_accepted_members(self):
        """Test coach retrieving accepted members"""
        self.relationship.status = "accepted"
        self.relationship.save()

        self.client.force_login(user=self.coach_user)

        # Use the correct URL name with hyphens
        url = reverse("accepted-members")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["memberId"], "M-00001")
        self.assertEqual(response.data[0]["name"], "member")

    def test_non_coach_cannot_access_coach_endpoints(self):
        """Test that non-coach users cannot access coach endpoints"""
        # Test with member user
        self.client.force_login(user=self.member_user)

        url = reverse("coach-member-requests")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse("accepted-members")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access coach endpoints"""
        url = reverse("coach-member-requests")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse("accepted-members")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
