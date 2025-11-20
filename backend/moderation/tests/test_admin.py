from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from moderation.models import Admin
from coach.models import Coach
from member.models import UserProfile
from django.utils import timezone


class AdminTestBase(TestCase):
    """Base setup for admin, coach, and member users."""

    def setUp(self):
        self.client = APIClient()

        # Admin user
        self.admin_user = User.objects.create_user(
            username="admin", password="adminpass", email="admin@admin.com"
        )
        self.admin_profile = self.admin_user.userprofile
        self.admin_profile.role = "admin"
        self.admin_profile.save()
        self.admin = Admin.objects.create(user=self.admin_user)

        # Coach user
        self.coach_user = User.objects.create_user(
            username="coach", password="coachpass", email="coach@hq.com"
        )
        self.coach_profile = self.coach_user.userprofile
        self.coach_profile.role = "coach"
        self.coach_profile.save()
        self.coach = Coach.objects.create(
            user=self.coach_profile,
            public_id="C-0001",
            status_approval="pending"
        )

        # Member user
        self.member_user = User.objects.create_user(
            username="member", password="memberpass", email="member@hq.com"
        )
        self.member_profile = self.member_user.userprofile
        self.member_profile.role = "member"
        self.member_profile.save()


class AdminCoachTests(AdminTestBase):

    def test_admin_can_approve_coach(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("approve_coach", kwargs={"coach_id": self.coach.pk})
        response = self.client.post(url, {"reason": "Valid credentials"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.coach.refresh_from_db()
        self.assertEqual(self.coach.status_approval, "approved")

    def test_admin_can_reject_coach(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("reject_coach", kwargs={"coach_id": self.coach.pk})
        response = self.client.post(url, {"reason": "Invalid credentials"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.coach.refresh_from_db()
        self.assertEqual(self.coach.status_approval, "rejected")

    def test_non_admin_cannot_approve_coach(self):
        self.client.force_authenticate(user=self.member_user)
        url = reverse("approve_coach", kwargs={"coach_id": self.coach.pk})
        response = self.client.post(url, {"reason": "Try to approve"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminUserManagementTests(AdminTestBase):

    def test_admin_can_delete_user(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("admin_delete_user", kwargs={"user_id": self.member_user.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=self.member_user.pk)

    def test_non_admin_cannot_delete_user(self):
        self.client.force_authenticate(user=self.member_user)
        url = reverse("admin_delete_user", kwargs={"user_id": self.coach_user.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_all_users_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("admin_list_users")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 2)  # coach + member
        usernames = [u["username"] for u in response.data]
        self.assertIn("coach", usernames)
        self.assertIn("member", usernames)

    def test_list_all_users_non_admin(self):
        self.client.force_authenticate(user=self.member_user)
        url = reverse("admin_list_users")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
