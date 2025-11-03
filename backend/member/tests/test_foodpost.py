from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from coach.models import Coach
from member.models import Member, FoodPost, FoodPostComment, CoachMemberRelationship


class FoodPostTests(TestCase):
    """Tests for FoodPost and FoodPostComment creation, update, deletion, and commenting."""

    def setUp(self):
        self.client = APIClient()

        # Create member user
        self.member_user = User.objects.create_user(
            username="member", password="pass123", email="member@example.com"
        )
        self.member_profile = self.member_user.userprofile
        self.member_profile.role = "member"
        self.member_profile.save()

        # Create coach user
        self.coach_user = User.objects.create_user(
            username="coach", password="coachpass", email="coach@example.com"
        )
        self.coach_profile = self.coach_user.userprofile
        self.coach_profile.role = "coach"
        self.coach_profile.save()

        self.coach = Coach.objects.create(
            user=self.coach_profile, status_approval="approved", public_id="C-00001"
        )

        self.member = Member.objects.create(
            user=self.member_profile, member_id="M-00001", status="approved"
        )

        # Create coach-member relationship
        CoachMemberRelationship.objects.create(
            coach=self.coach, member=self.member, status="accepted"
        )

        # Create initial food post
        self.food_post = FoodPost.objects.create(
            user_profile=self.member_profile,
            coach=self.coach_profile,
            title="Test Post",
            content="This is a test food post.",
        )

        # Log in as member user by default
        self.client.force_login(self.member_user)

    def test_food_post_creation_as_member(self):
        """Test member can create a food post"""
        url = reverse("food-posts")
        data = {
            "title": "Healthy Salad",
            "content": "This is a recipe for a healthy salad.",
            "coach": self.coach_profile.id,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FoodPost.objects.count(), 2)
        self.assertEqual(response.data["title"], "Healthy Salad")
        self.assertEqual(
            response.data["author_name"], self.member_profile.user.username
        )

    def test_food_post_creation_as_normal_user(self):
        """Test normal user cannot create a food post"""
        normal_user = User.objects.create_user(
            username="normaluser", password="normalpass", email="normaluser@example.com"
        )
        normal_profile = normal_user.userprofile
        normal_profile.role = "normal"
        normal_profile.save()

        self.client.force_login(normal_user)

        url = reverse("food-posts")
        data = {
            "title": "Healthy Salad",
            "content": "This is a recipe for a healthy salad.",
            "coach": self.coach_profile.id,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(FoodPost.objects.count(), 1)  # Only the initial post

    def test_food_post_creation_missing_required_fields(self):
        """Test food post creation fails with missing required fields"""
        url = reverse("food-posts")
        data = {
            "title": "Incomplete Post",
            # Missing 'content' field
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("content", response.data)

    def test_food_post_list_as_member(self):
        """Test member can list their food posts"""
        url = reverse("food-posts")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Post")

    def test_food_post_list_as_coach(self):
        """Test coach can list food posts from their members"""
        self.client.force_login(self.coach_user)

        url = reverse("food-posts")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Post")

    def test_food_post_ordering(self):
        """Test that food posts are ordered by creation date descending"""
        # Create additional posts
        post2 = FoodPost.objects.create(
            user_profile=self.member_profile,
            coach=self.coach_profile,
            title="Second Post",
            content="Second post content",
        )

        post3 = FoodPost.objects.create(
            user_profile=self.member_profile,
            coach=self.coach_profile,
            title="Third Post",
            content="Third post content",
        )

        url = reverse("food-posts")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        # Should be ordered by created_at descending (newest first)
        self.assertEqual(response.data[0]["title"], "Third Post")
        self.assertEqual(response.data[1]["title"], "Second Post")
        self.assertEqual(response.data[2]["title"], "Test Post")

    def test_food_post_update_as_owner(self):
        """Test member can update their own food post"""
        url = reverse("food-post-update", kwargs={"id": self.food_post.id})
        data = {
            "title": "Updated Test Post",
            "content": "This is an updated test food post.",
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.food_post.refresh_from_db()
        self.assertEqual(self.food_post.title, "Updated Test Post")
        self.assertEqual(self.food_post.content, "This is an updated test food post.")

    def test_food_post_partial_update_as_owner(self):
        """Test member can partially update their own food post"""
        url = reverse("food-post-update", kwargs={"id": self.food_post.id})
        data = {
            "title": "Partially Updated Post",
        }
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.food_post.refresh_from_db()
        self.assertEqual(self.food_post.title, "Partially Updated Post")
        # Content should remain unchanged
        self.assertEqual(self.food_post.content, "This is a test food post.")

    def test_food_post_update_by_other_member(self):
        """Test that other members cannot update the food post"""
        other_user = User.objects.create_user(
            username="otheruser", password="otherpass", email="otheruser@example.com"
        )
        other_profile = other_user.userprofile
        other_profile.role = "member"
        other_profile.save()

        self.client.force_login(other_user)

        url = reverse("food-post-update", kwargs={"id": self.food_post.id})
        data = {
            "title": "Malicious Update",
            "content": "This update should not be allowed.",
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.food_post.refresh_from_db()
        self.assertNotEqual(self.food_post.title, "Malicious Update")

    def test_food_post_update_by_coach(self):
        """Test coach cannot update member's food post"""
        self.client.force_login(self.coach_user)

        url = reverse("food-post-update", kwargs={"id": self.food_post.id})
        data = {
            "title": "Coach Update Attempt",
            "content": "Coach should not be able to update.",
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.food_post.refresh_from_db()
        self.assertNotEqual(self.food_post.title, "Coach Update Attempt")

    def test_food_post_delete_as_owner(self):
        """Test member can delete their own food post"""
        url = reverse("food-post-delete", kwargs={"id": self.food_post.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FoodPost.objects.count(), 0)

    def test_food_post_delete_by_other_member(self):
        """Test that other members cannot delete the food post"""
        other_user = User.objects.create_user(
            username="otheruser", password="otherpass", email="otheruser@example.com"
        )
        other_profile = other_user.userprofile
        other_profile.role = "member"
        other_profile.save()

        self.client.force_login(other_user)

        url = reverse("food-post-delete", kwargs={"id": self.food_post.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(FoodPost.objects.count(), 1)

    def test_food_post_delete_nonexistent(self):
        """Test deleting a non-existent food post returns 404"""
        url = reverse("food-post-delete", kwargs={"id": 9999})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_food_post_comment_by_assigned_coach(self):
        """Test assigned coach can comment on food post"""
        self.client.force_login(self.coach_user)

        url = reverse("food-post-comments", kwargs={"post_id": self.food_post.id})
        data = {"text": "Great job on your food post!"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FoodPostComment.objects.count(), 1)

        comment = FoodPostComment.objects.first()
        self.assertEqual(comment.text, "Great job on your food post!")
        self.assertEqual(comment.author, self.coach_profile)
        self.assertEqual(comment.food_post, self.food_post)

    def test_food_post_comment_by_member_owner(self):
        """Test member can comment on their own food post"""
        url = reverse("food-post-comments", kwargs={"post_id": self.food_post.id})
        data = {"text": "This is a comment from the member."}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FoodPostComment.objects.count(), 1)

        comment = FoodPostComment.objects.first()
        self.assertEqual(comment.author, self.member_profile)

    def test_food_post_comment_by_non_assigned_coach(self):
        """Test that non-assigned coach cannot comment on food post"""
        other_coach_user = User.objects.create_user(
            username="othercoach", password="otherpass", email="othercoach@example.com"
        )
        other_coach_profile = other_coach_user.userprofile
        other_coach_profile.role = "coach"
        other_coach_profile.save()

        # Create coach but no relationship with member
        Coach.objects.create(
            user=other_coach_profile, status_approval="approved", public_id="C-00002"
        )

        self.client.force_login(other_coach_user)

        url = reverse("food-post-comments", kwargs={"post_id": self.food_post.id})
        data = {"text": "Comment from non-assigned coach"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(FoodPostComment.objects.count(), 0)

    def test_food_post_comment_by_other_member(self):
        """Test that other members cannot comment on the food post"""
        other_user = User.objects.create_user(
            username="othermember",
            password="otherpass",
            email="othermember@example.com",
        )
        other_profile = other_user.userprofile
        other_profile.role = "member"
        other_profile.save()

        self.client.force_login(other_user)

        url = reverse("food-post-comments", kwargs={"post_id": self.food_post.id})
        data = {"text": "Comment from other member"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(FoodPostComment.objects.count(), 0)

    def test_food_post_comment_list(self):
        """Test listing comments for a food post"""
        # Create some comments first
        FoodPostComment.objects.create(
            food_post=self.food_post, author=self.coach_profile, text="Coach comment"
        )
        FoodPostComment.objects.create(
            food_post=self.food_post, author=self.member_profile, text="Member comment"
        )

        url = reverse("food-post-comments", kwargs={"post_id": self.food_post.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Comments should be ordered by created_at ascending
        self.assertEqual(response.data[0]["text"], "Coach comment")
        self.assertEqual(response.data[1]["text"], "Member comment")

    def test_food_post_comment_missing_text(self):
        """Test comment creation fails with missing text"""
        url = reverse("food-post-comments", kwargs={"post_id": self.food_post.id})
        data = {}  # Missing text field
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("text", response.data)

    def test_comment_update_by_author(self):
        """Test comment author can update their comment"""
        comment = FoodPostComment.objects.create(
            food_post=self.food_post, author=self.coach_profile, text="Original comment"
        )

        self.client.force_login(self.coach_user)

        url = reverse(
            "food-post-comment-detail",
            kwargs={"post_id": self.food_post.id, "comment_id": comment.id},
        )
        data = {"text": "Updated comment"}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.text, "Updated comment")

    def test_comment_delete_by_author(self):
        """Test comment author can delete their comment"""
        comment = FoodPostComment.objects.create(
            food_post=self.food_post,
            author=self.coach_profile,
            text="Comment to delete",
        )

        self.client.force_login(self.coach_user)

        url = reverse(
            "food-post-comment-detail",
            kwargs={"post_id": self.food_post.id, "comment_id": comment.id},
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FoodPostComment.objects.count(), 0)

    def test_comment_update_by_non_author(self):
        """Test non-author cannot update comment"""
        comment = FoodPostComment.objects.create(
            food_post=self.food_post, author=self.coach_profile, text="Original comment"
        )

        # Try to update as member (not the author)
        url = reverse(
            "food-post-comment-detail",
            kwargs={"post_id": self.food_post.id, "comment_id": comment.id},
        )
        data = {"text": "Unauthorized update"}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        comment.refresh_from_db()
        self.assertEqual(comment.text, "Original comment")


class FoodPostImageTests(TestCase):
    """Tests for food post image upload functionality"""

    def setUp(self):
        self.client = APIClient()

        # Create member and food post
        self.member_user = User.objects.create_user(
            username="member", password="pass123"
        )
        self.member_profile = self.member_user.userprofile
        self.member_profile.role = "member"
        self.member_profile.save()

        self.coach_user = User.objects.create_user(
            username="coach", password="coachpass"
        )
        self.coach_profile = self.coach_user.userprofile
        self.coach_profile.role = "coach"
        self.coach_profile.save()

        self.food_post = FoodPost.objects.create(
            user_profile=self.member_profile,
            coach=self.coach_profile,
            title="Test Post",
            content="Test content",
        )

        self.client.force_login(self.member_user)

    def test_image_upload(self):
        """Test image upload to food post"""
        url = reverse("upload-food-post-image", kwargs={"id": self.food_post.id})
        image = SimpleUploadedFile(
            "mock_image.jpg", b"fake image content", content_type="image/jpeg"
        )
        response = self.client.post(url, {"image": image}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_image_upload_by_non_owner(self):
        """Test non-owner cannot upload image"""
        other_user = User.objects.create_user(username="other", password="otherpass")
        other_profile = other_user.userprofile
        other_profile.role = "member"
        other_profile.save()

        self.client.force_login(other_user)

        url = reverse("upload-food-post-image", kwargs={"id": self.food_post.id})
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
