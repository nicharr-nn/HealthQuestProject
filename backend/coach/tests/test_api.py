from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User, UserProfile
from coach.models import Coach


class CoachAPITests(TestCase):
    """Tests for Coach API endpoints."""

    def setUp(self):
        """Set up test data and client."""
        self.client = APIClient()

        # Users
        self.user1 = User.objects.create_user(username="coach1", password="pass123")
        self.profile1, _ = UserProfile.objects.get_or_create(user=self.user1)

        self.user2 = User.objects.create_user(username="coach2", password="pass123")
        self.profile2, _ = UserProfile.objects.get_or_create(user=self.user2)

        # URLs
        self.upload_url = reverse("upload_certification")
        self.status_url = reverse("coach_status")
        self.edit_url = reverse("edit_coach_profile")

        self.client.force_authenticate(self.user1)

    def test_post_upload_certification_creates_coach(self):
        """Test uploading certification creates a new coach profile."""
        file = SimpleUploadedFile("cert.pdf", b"filecontent", content_type="application/pdf")
        payload = {"bio": "This is my bio", "certification_doc": file}

        response = self.client.post(self.upload_url, payload, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["bio"], "This is my bio")
        self.assertEqual(response.data["status_approval"], "pending")
        self.assertTrue(Coach.objects.filter(user=self.profile1).exists())

    def test_post_upload_certification_updates_if_exists(self):
        """Test uploading certification updates existing coach profile."""
        coach = Coach.objects.create(user=self.profile1, bio="Old bio")

        response = self.client.post(self.upload_url, {"bio": "New bio"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        coach.refresh_from_db()
        self.assertEqual(coach.bio, "New bio")

    def test_patch_upload_certification_updates(self):
        """"Test patching certification updates coach profile."""
        coach = Coach.objects.create(user=self.profile1, bio="Original Bio")
        file = SimpleUploadedFile("new.pdf", b"newcontent", content_type="application/pdf")
        payload = {"bio": "Updated Bio", "certification_doc": file}

        response = self.client.patch(self.upload_url, payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        coach.refresh_from_db()
        self.assertEqual(coach.bio, "Updated Bio")
        self.assertEqual(coach.status_approval, "pending")
        self.assertIsNone(coach.approved_date)

    def test_patch_upload_certification_not_found(self):
        """Test patching certification for non-existent coach returns 404."""
        response = self.client.patch(self.upload_url, {"bio": "Test"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_coach_status_existing(self):
        """Test retrieving existing coach status."""
        Coach.objects.create(user=self.profile1, bio="A Bio")

        response = self.client.get(self.status_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["coach"]["bio"], "A Bio")


    def test_coach_status_no_coach(self):
        """Test retrieving coach status when no coach profile exists."""
        response = self.client.get(self.status_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data["coach"])

    def test_edit_coach_profile_updates_bio(self):
        """Test editing coach profile updates the bio."""
        coach = Coach.objects.create(user=self.profile1, bio="Old Bio")

        response = self.client.put(self.edit_url, {"bio": "Updated Bio"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        coach.refresh_from_db()
        self.assertEqual(coach.bio, "Updated Bio")

    def test_edit_coach_profile_error(self):
        """Test editing coach profile returns error if no coach exists."""
        self.profile1.delete()

        response = self.client.put(self.edit_url, {"bio": "Test"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_large_file(self):
        """Test uploading a large certification document."""
        content = b"a" * (5 * 1024 * 1024)  # 5 MB
        file = SimpleUploadedFile("cert.pdf", content, content_type="application/pdf")
        response = self.client.post(self.upload_url, {"certification_doc": file}, format="multipart")
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
