from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from moderation.models import Admin
from coach.models import Coach


class AdminTestBase(TestCase):
    """Base setup for admin, coach, and member users."""

    def setUp(self):
        """Set up users and profiles for testing."""
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
            user=self.coach_profile, public_id="C-0001", status_approval="pending"
        )

        # Member user
        self.member_user = User.objects.create_user(
            username="member", password="memberpass", email="member@hq.com"
        )
        self.member_profile = self.member_user.userprofile
        self.member_profile.role = "member"
        self.member_profile.save()
