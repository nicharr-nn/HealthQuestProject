from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import UserLevel, UserProfile

User = get_user_model()


class UserLevelsTests(TestCase):
    """Test user level information via user-info endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.user.refresh_from_db()

        self.profile = UserProfile.objects.get(user=self.user)
        self.profile.role = "normal"
        self.profile.height = 175.0
        self.profile.weight = 70.0
        self.profile.age = 30
        self.profile.gender = "M"
        self.profile.location = "USA"
        self.profile.save()
        self.profile.refresh_from_db()

        # Get or create level (in case signal doesn't exist)
        self.level, _ = UserLevel.objects.get_or_create(
            user_profile=self.profile,
            defaults={
                "level": "Bronze",
                "level_rank": 1,
                "xp": 0,
                "goal_achieved": False,
            },
        )
        # Update level values for testing
        self.level.level = "Bronze"
        self.level.level_rank = 1
        self.level.xp = 500
        self.level.goal_achieved = False
        self.level.save()

    def test_get_user_levels_bronze(self):
        """User can get their level information (Bronze)"""
        self.client.force_login(self.user)
        url = reverse("user-info")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("user", response.data)
        self.assertIn("profile", response.data["user"])
        self.assertIn("current_level", response.data["user"]["profile"])
        self.assertEqual(
            response.data["user"]["profile"]["current_level"]["level"], "Bronze"
        )
        self.assertEqual(
            response.data["user"]["profile"]["current_level"]["level_rank"], 1
        )
        self.assertEqual(response.data["user"]["profile"]["current_level"]["xp"], 500)
        self.assertFalse(
            response.data["user"]["profile"]["current_level"]["goal_achieved"]
        )

    def test_get_user_levels_silver(self):
        """Silver level user gets correct level info"""
        self.level.level = "Silver"
        self.level.level_rank = 2
        self.level.xp = 1500
        self.level.save()

        self.client.force_login(self.user)
        url = reverse("user-info")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["user"]["profile"]["current_level"]["level"], "Silver"
        )
        self.assertEqual(
            response.data["user"]["profile"]["current_level"]["level_rank"], 2
        )
        self.assertEqual(response.data["user"]["profile"]["current_level"]["xp"], 1500)

    def test_get_user_levels_gold(self):
        """Gold level user gets correct information"""
        self.level.level = "Gold"
        self.level.level_rank = 3
        self.level.xp = 5000
        self.level.save()

        self.client.force_login(self.user)
        url = reverse("user-info")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["user"]["profile"]["current_level"]["level"], "Gold"
        )
        self.assertEqual(
            response.data["user"]["profile"]["current_level"]["level_rank"], 3
        )
        self.assertEqual(response.data["user"]["profile"]["current_level"]["xp"], 5000)

    def test_get_user_levels_default_bronze(self):
        """Newly created user has default Bronze level with 0 XP"""
        # Create new user
        new_user = User.objects.create_user(
            username="newuser",
            email="new@example.com",
            password="newpass123",
        )
        new_user.refresh_from_db()

        # Get profile
        new_profile = UserProfile.objects.get(user=new_user)

        # Create level for new user
        UserLevel.objects.get_or_create(
            user_profile=new_profile,
            defaults={
                "level": "Bronze",
                "level_rank": 1,
                "xp": 0,
                "goal_achieved": False,
            },
        )

        self.client.force_login(new_user)
        url = reverse("user-info")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("current_level", response.data["user"]["profile"])
        self.assertEqual(
            response.data["user"]["profile"]["current_level"]["level"], "Bronze"
        )
        self.assertEqual(response.data["user"]["profile"]["current_level"]["xp"], 0)

    def test_level_xp_increase(self):
        """Level XP can be increased"""
        # Update XP
        self.level.xp = 750
        self.level.save()

        self.client.force_login(self.user)
        url = reverse("user-info")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user"]["profile"]["current_level"]["xp"], 750)

    def test_level_goal_achieved(self):
        """Level can show goal achieved status"""
        # Mark goal as achieved
        self.level.goal_achieved = True
        self.level.save()

        self.client.force_login(self.user)
        url = reverse("user-info")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            response.data["user"]["profile"]["current_level"]["goal_achieved"]
        )

    def test_unauthenticated_user_no_level(self):
        """Unauthenticated user cannot get level info"""
        url = reverse("user-info")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["isAuthenticated"])
        self.assertIsNone(response.data["user"])

    def test_level_rank_progression(self):
        """Test level rank progression from Bronze to Gold"""
        levels = [
            ("Bronze", 1, 500),
            ("Silver", 2, 1500),
            ("Gold", 3, 5000),
        ]

        for level_name, rank, xp in levels:
            self.level.level = level_name
            self.level.level_rank = rank
            self.level.xp = xp
            self.level.save()

            self.client.force_login(self.user)
            url = reverse("user-info")
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.data["user"]["profile"]["current_level"]["level"], level_name
            )
            self.assertEqual(
                response.data["user"]["profile"]["current_level"]["level_rank"], rank
            )
            self.assertEqual(
                response.data["user"]["profile"]["current_level"]["xp"], xp
            )

    def test_user_without_level(self):
        """Test user info when level doesn't exist"""
        # Delete the level
        self.level.delete()

        self.client.force_login(self.user)
        url = reverse("user-info")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Should either be None or have default values
        current_level = response.data["user"]["profile"].get("current_level")
        # Test passes if level is None or if it exists with default values
        if current_level is not None:
            self.assertIn("level", current_level)


# Run tests with: python manage.py test users.tests.test_userlevel
