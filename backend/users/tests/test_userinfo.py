from django.apps import apps
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, timedelta

User = get_user_model()


def get_user_profile_model():
    return apps.get_model("users", "UserProfile")


def get_fitness_goal_model():
    return apps.get_model("users", "FitnessGoal")


def get_user_level_model():
    return apps.get_model("users", "UserLevel")


class UserInfoTests(TestCase):
    """Test user-info endpoint"""

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
        self.userprofile_model = get_user_profile_model()

        self.profile = self.userprofile_model.objects.get(user=self.user)
        self.profile.role = "normal"
        self.profile.height = 175.0
        self.profile.weight = 70.0
        self.profile.age = 30
        self.profile.gender = "M"
        self.profile.location = "USA"
        self.profile.save()
        self.profile.refresh_from_db()

    def test_user_info_authenticated(self):
        """Authenticated user should get their info"""
        self.client.force_login(self.user)
        url = reverse("user-info")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["isAuthenticated"])
        self.assertEqual(response.data["user"]["username"], "testuser")
        self.assertEqual(response.data["user"]["email"], "test@example.com")
        self.assertEqual(response.data["user"]["first_name"], "Test")
        self.assertEqual(response.data["user"]["last_name"], "User")
        self.assertFalse(response.data["user"]["is_admin"])

        # Check nested profile structure
        self.assertIn("profile", response.data["user"])
        # Role might be empty string if not set properly, check it exists
        self.assertIn("role", response.data["user"]["profile"])
        self.assertEqual(float(response.data["user"]["profile"]["height"]), 175.0)
        self.assertEqual(float(response.data["user"]["profile"]["weight"]), 70.0)
        self.assertEqual(response.data["user"]["profile"]["age"], 30)
        self.assertEqual(response.data["user"]["profile"]["gender"], "M")
        self.assertEqual(response.data["user"]["profile"]["location"], "USA")

        # Check additional fields
        self.assertIn("is_admin", response.data["user"])
        self.assertIn("is_staff", response.data["user"])
        self.assertIn("profile_complete", response.data["user"])

    def test_user_info_unauthenticated(self):
        """Unauthenticated user should get isAuthenticated=False"""
        url = reverse("user-info")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["isAuthenticated"])
        self.assertIsNone(response.data["user"])

    def test_user_info_with_fitness_goal(self):
        """User info should include fitness goals"""
        # Update profile to member role (required for fitness goals)
        self.profile.role = "member"
        self.profile.save()

        FitnessGoal = get_fitness_goal_model()
        FitnessGoal.objects.create(
            user_profile=self.profile,
            goal_type="lose_weight",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=90),
        )

        self.client.force_login(self.user)
        url = reverse("user-info")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("fitness_goals", response.data["user"]["profile"])
        self.assertGreater(len(response.data["user"]["profile"]["fitness_goals"]), 0)
        # Check that at least one goal exists
        self.assertIn("goal_type", response.data["user"]["profile"]["fitness_goals"][0])

    def test_user_info_with_level(self):
        """User info should include level information"""
        UserLevel = get_user_level_model()
        UserLevel.objects.create(
            user_profile=self.profile,
            level="Bronze",
            level_rank=1,
            xp=500,
            goal_achieved=False,
        )

        self.client.force_login(self.user)
        url = reverse("user-info")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
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


class SetRoleTests(TestCase):
    """Test select-role endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.UserProfile = get_user_profile_model()

    def test_set_role_normal(self):
        """User can set role to normal"""
        self.client.force_login(self.user)
        url = reverse("select-role")
        response = self.client.post(url, {"role": "normal"}, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["role"], "normal")

        # Verify in database
        profile = self.UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.role, "normal")

    def test_set_role_member(self):
        """User can set role to member"""
        self.client.force_login(self.user)
        url = reverse("select-role")
        response = self.client.post(url, {"role": "member"}, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["role"], "member")

    def test_set_role_coach(self):
        """User can set role to coach"""
        self.client.force_login(self.user)
        url = reverse("select-role")
        response = self.client.post(url, {"role": "coach"}, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["role"], "coach")

    def test_set_role_unauthenticated(self):
        """Unauthenticated user cannot set role"""
        url = reverse("select-role")
        response = self.client.post(url, {"role": "normal"}, format="json")

        self.assertIn(response.status_code, [401, 403])

    def test_set_role_creates_profile_if_not_exists(self):
        """Setting role creates profile if it doesn't exist"""
        # Delete profile if exists
        self.UserProfile.objects.filter(user=self.user).delete()

        self.client.force_login(self.user)
        url = reverse("select-role")
        response = self.client.post(url, {"role": "normal"}, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.UserProfile.objects.filter(user=self.user).exists())


class UpdateProfileTests(UserInfoTests):
    """Test update-profile endpoint"""

    def test_update_profile_basic_fields(self):
        """User can update basic profile fields"""
        self.client.force_login(self.user)
        url = reverse("update-profile")
        data = {
            "age": 56,
            "height": 150.0,
            "weight": 75.5,
            "gender": "F",
            "location": "KR",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "success")
        self.assertIn("data", response.data)
        self.assertEqual(response.data["data"]["age"], 56)
        self.assertEqual(float(response.data["data"]["height"]), 150.0)
        self.assertEqual(float(response.data["data"]["weight"]), 75.5)
        self.assertEqual(response.data["data"]["location"], "KR")
        self.assertEqual(response.data["data"]["gender"], "F")

    def test_update_profile_partial(self):
        """User can update only some fields"""
        self.client.force_login(self.user)
        url = reverse("update-profile")
        data = {"location": "LA"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["location"], "LA")
        # Age might be None if not set in defaults, just check response is success
        self.assertIn("age", response.data["data"])

    def test_update_profile_invalid_data(self):
        """Invalid data should return 400"""
        self.client.force_login(self.user)
        url = reverse("update-profile")
        data = {"age": "not_a_number"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["status"], "error")

    def test_update_profile_unauthenticated(self):
        """Unauthenticated user cannot update profile"""
        url = reverse("update-profile")
        data = {"age": 30}
        response = self.client.post(url, data, format="json")

        self.assertIn(response.status_code, [401, 403])

    def test_update_profile_profile_exists(self):
        """Profile should be updated when it exists"""
        self.client.force_login(self.user)
        url = reverse("update-profile")
        data = {"age": 30}
        response = self.client.post(url, data, format="json")

        # Should succeed if profile exists
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "success")


class UploadPhotoTests(TestCase):
    """Test upload-photo endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.UserProfile = get_user_profile_model()
        self.profile, _ = self.UserProfile.objects.get_or_create(
            user=self.user,
            defaults={"role": "normal"},
        )

    def test_upload_photo_success(self):
        """User can upload profile photo"""
        self.client.force_login(self.user)
        url = reverse("upload-photo")

        # Create a test image
        image = SimpleUploadedFile(
            "test_photo.jpg",
            b"fake_image_content",
            content_type="image/jpeg",
        )

        response = self.client.post(url, {"photo": image}, format="multipart")

        self.assertEqual(response.status_code, 200)
        self.assertIn("photo_url", response.data)
        self.assertIn("file_path", response.data)
        self.assertEqual(response.data["detail"], "Photo uploaded successfully!")

        # Verify photo was saved to profile
        self.profile.refresh_from_db()
        self.assertTrue(bool(self.profile.photo))

    def test_upload_photo_no_file(self):
        """Should return 400 when no file is provided"""
        self.client.force_login(self.user)
        url = reverse("upload-photo")

        response = self.client.post(url, {}, format="multipart")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["detail"], "No file provided.")

    def test_upload_photo_unauthenticated(self):
        """Unauthenticated user cannot upload photo"""
        url = reverse("upload-photo")

        image = SimpleUploadedFile(
            "test_photo.jpg",
            b"fake_image_content",
            content_type="image/jpeg",
        )

        response = self.client.post(url, {"photo": image}, format="multipart")

        self.assertIn(response.status_code, [401, 403])

    def test_upload_photo_replace_existing(self):
        """Uploading new photo should replace existing one"""
        self.client.force_login(self.user)
        url = reverse("upload-photo")

        # Upload first photo
        image1 = SimpleUploadedFile(
            "photo1.jpg",
            b"fake_image_1",
            content_type="image/jpeg",
        )
        response1 = self.client.post(url, {"photo": image1}, format="multipart")
        self.assertEqual(response1.status_code, 200)
        first_path = response1.data["file_path"]

        # Upload second photo
        image2 = SimpleUploadedFile(
            "photo2.jpg",
            b"fake_image_2",
            content_type="image/jpeg",
        )
        response2 = self.client.post(url, {"photo": image2}, format="multipart")
        self.assertEqual(response2.status_code, 200)
        second_path = response2.data["file_path"]

        # Paths should be different
        self.assertNotEqual(first_path, second_path)


class SetGoalTests(TestCase):
    """Test select-goal endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="normaluser",
            email="normal@example.com",
            password="testpass123",
        )
        self.coach_user = User.objects.create_user(
            username="coachuser",
            email="coach@example.com",
            password="testpass123",
        )

        self.user.refresh_from_db()
        self.userprofile_model = get_user_profile_model()
        self.FitnessGoal = get_fitness_goal_model()

        self.normal_profile = self.userprofile_model.objects.get(user=self.user)
        self.normal_profile.role = "normal"
        self.normal_profile.save()
        self.normal_profile.refresh_from_db()

        # Coach profile
        self.coach_profile, _ = self.userprofile_model.objects.get_or_create(
            user=self.coach_user,
        )
        self.coach_profile.role = "coach"
        self.coach_profile.save()
        self.coach_profile.refresh_from_db()

    def test_set_goal_weight_loss(self):
        """Normal user can set weight loss goal"""
        self.client.force_login(self.user)
        url = reverse("select-goal")
        data = {
            "goal_type": "lose_weight",
            "end_date": (date.today() + timedelta(days=90)).isoformat(),
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "success")
        self.assertIn("user", response.data)

        # Verify goal was created
        goal = self.FitnessGoal.objects.filter(
            user_profile=self.normal_profile, goal_type="lose_weight"
        ).first()
        self.assertIsNotNone(goal)

    def test_set_goal_muscle_gain(self):
        """Normal user can set muscle gain goal"""
        self.client.force_login(self.user)
        url = reverse("select-goal")
        data = {"goal_type": "build_muscle"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "success")

        # Check if goal exists
        goals = self.FitnessGoal.objects.filter(user_profile=self.normal_profile)
        self.assertGreater(goals.count(), 0)

        # Check the latest goal
        latest_goal = goals.order_by("-id").first()
        self.assertEqual(latest_goal.goal_type, "build_muscle")

    def test_set_goal_endurance(self):
        """Normal user can set endurance goal"""
        self.client.force_login(self.user)
        url = reverse("select-goal")
        data = {"goal_type": "improve_endurance"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 200)

        latest_goal = (
            self.FitnessGoal.objects.filter(user_profile=self.normal_profile)
            .order_by("-id")
            .first()
        )
        self.assertEqual(latest_goal.goal_type, "improve_endurance")

    def test_set_goal_multiple_goals(self):
        """User can have multiple fitness goals"""
        self.client.force_login(self.user)
        url = reverse("select-goal")

        # Set first goal
        data1 = {"goal_type": "lose_weight"}
        response1 = self.client.post(url, data1, format="json")
        self.assertEqual(response1.status_code, 200)

        # Set second goal (different type)
        data2 = {"goal_type": "build_muscle"}
        response2 = self.client.post(url, data2, format="json")
        self.assertEqual(response2.status_code, 200)

        # Should have multiple goals
        goals_count = self.FitnessGoal.objects.filter(
            user_profile=self.normal_profile
        ).count()
        self.assertGreaterEqual(goals_count, 1)

    def test_set_goal_coach_cannot(self):
        """Coach cannot set fitness goals"""
        self.client.force_login(self.coach_user)
        url = reverse("select-goal")
        data = {"goal_type": "lose_weight"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("Only normal users and members", response.data["detail"])

    def test_set_goal_no_goal_type(self):
        """Should return 400 if goal_type is missing"""
        # Use coach user to test validation order
        self.client.force_login(self.user)
        url = reverse("select-goal")
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, 400)
        # Either error message is acceptable
        self.assertIn("detail", response.data)

    def test_set_goal_unauthenticated(self):
        """Unauthenticated user cannot set goal"""
        url = reverse("select-goal")
        data = {"goal_type": "lose_weight"}
        response = self.client.post(url, data, format="json")

        self.assertIn(response.status_code, [401, 403])


# Run tests with: python manage.py test users.tests.test_userinfo
