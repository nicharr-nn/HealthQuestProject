from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from member.models import Member, CoachMemberRelationship, FoodPost, FoodPostComment
from coach.models import Coach

User = get_user_model()


class FoodPostCommentTests(TestCase):
    """Test food post comments functionality"""

    def setUp(self):
        self.client = APIClient()

        # Create Coach
        self.coach_user = User.objects.create_user(
            username="testcoach", email="coach@test.com", password="testpass123"
        )
        self.coach_profile = self.coach_user.userprofile
        self.coach_profile.role = "coach"
        self.coach_profile.save()

        self.coach = Coach.objects.create(
            user=self.coach_profile,
            public_id=f"C-{self.coach_user.id:05d}",
            status_approval="approved",
        )

        # Create Member
        self.member_user = User.objects.create_user(
            username="testmember", email="member@test.com", password="testpass123"
        )
        self.member_profile = self.member_user.userprofile
        self.member_profile.role = "member"
        self.member_profile.save()

        self.member = Member.objects.create(
            user=self.member_profile,
            member_id=f"M-{self.member_user.id:05d}",
            experience_level="beginner",
            status="approved",
        )

        # Create Coach-Member Relationship
        self.relationship = CoachMemberRelationship.objects.create(
            coach=self.coach, member=self.member, status="accepted"
        )

        # Create another coach for the other member
        self.other_coach_user = User.objects.create_user(
            username="othercoach", email="othercoach@test.com", password="testpass123"
        )
        self.other_coach_profile = self.other_coach_user.userprofile
        self.other_coach_profile.role = "coach"
        self.other_coach_profile.save()

        self.other_coach = Coach.objects.create(
            user=self.other_coach_profile,
            public_id=f"C-{self.other_coach_user.id:05d}",
            status_approval="approved",
        )

        # Create another member (not assigned to self.coach)
        self.other_member_user = User.objects.create_user(
            username="othermember", email="other@test.com", password="testpass123"
        )
        self.other_member_profile = self.other_member_user.userprofile
        self.other_member_profile.role = "member"
        self.other_member_profile.save()

        self.other_member = Member.objects.create(
            user=self.other_member_profile,
            member_id=f"M-{self.other_member_user.id:05d}",
            experience_level="intermediate",
            status="approved",
        )

        # Create relationship between other_coach and other_member
        self.other_relationship = CoachMemberRelationship.objects.create(
            coach=self.other_coach, member=self.other_member, status="accepted"
        )

        # Create Food Post by member (assigned to self.coach)
        self.food_post = FoodPost.objects.create(
            user_profile=self.member_profile,
            coach=self.coach_profile,
            title="My Breakfast",
            content="Healthy oatmeal with fruits",
        )

        # Create Food Post by other member (assigned to other_coach)
        self.other_food_post = FoodPost.objects.create(
            user_profile=self.other_member_profile,
            coach=self.other_coach_profile,
            title="Other's Lunch",
            content="Grilled chicken salad",
        )

    def test_member_can_comment_on_own_post(self):
        """Member can comment on their own food post"""
        self.client.force_login(self.member_user)

        url = reverse("food-post-comments", kwargs={"post_id": self.food_post.id})
        data = {
            "text": "This was delicious!",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["text"], "This was delicious!")
        self.assertEqual(response.data["author_name"], self.member_user.username)
        self.assertEqual(response.data["author_role"], "member")

        # Verify comment was created
        self.assertEqual(FoodPostComment.objects.count(), 1)
        comment = FoodPostComment.objects.first()
        self.assertEqual(comment.food_post, self.food_post)
        self.assertEqual(comment.author, self.member_profile)

    def test_member_cannot_comment_on_others_post(self):
        """Member cannot comment on another member's post"""
        self.client.force_login(self.member_user)

        url = reverse("food-post-comments", kwargs={"post_id": self.other_food_post.id})
        data = {
            "text": "Nice meal!",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(
            "Members may only comment on their own posts", response.data["error"]
        )
        self.assertEqual(FoodPostComment.objects.count(), 0)

    def test_coach_can_comment_on_assigned_member_post(self):
        """Coach can comment on their assigned member's post"""
        self.client.force_login(self.coach_user)

        url = reverse("food-post-comments", kwargs={"post_id": self.food_post.id})
        data = {
            "text": "Great choice! Very nutritious.",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["text"], "Great choice! Very nutritious.")
        self.assertEqual(response.data["author_name"], self.coach_user.username)
        self.assertEqual(response.data["author_role"], "coach")

        # Verify comment was created
        comment = FoodPostComment.objects.first()
        self.assertEqual(comment.author, self.coach_profile)

    def test_coach_cannot_comment_on_unassigned_member_post(self):
        """Coach cannot comment on a post from member they're not assigned to"""
        self.client.force_login(self.coach_user)

        url = reverse("food-post-comments", kwargs={"post_id": self.other_food_post.id})
        data = {
            "text": "Good meal!",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("not the assigned coach", response.data["error"])

    def test_get_comments_for_post(self):
        """Get all comments for a food post"""
        # Create some comments
        FoodPostComment.objects.create(
            food_post=self.food_post,
            author=self.member_profile,
            text="My own comment",
        )
        FoodPostComment.objects.create(
            food_post=self.food_post,
            author=self.coach_profile,
            text="Coach feedback",
        )

        self.client.force_login(self.member_user)
        url = reverse("food-post-comments", kwargs={"post_id": self.food_post.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Check comment details
        comments_text = [c["text"] for c in response.data]
        self.assertIn("My own comment", comments_text)
        self.assertIn("Coach feedback", comments_text)

    def test_update_own_comment(self):
        """User can update their own comment"""
        comment = FoodPostComment.objects.create(
            food_post=self.food_post,
            author=self.coach_profile,
            text="Original feedback",
        )

        self.client.force_login(self.coach_user)
        url = reverse(
            "food-post-comment-detail",
            kwargs={"post_id": self.food_post.id, "comment_id": comment.id},
        )

        data = {
            "text": "Updated feedback",
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], "Updated feedback")

        # Verify in database
        comment.refresh_from_db()
        self.assertEqual(comment.text, "Updated feedback")

    def test_cannot_update_others_comment(self):
        """User cannot update someone else's comment"""
        comment = FoodPostComment.objects.create(
            food_post=self.food_post,
            author=self.coach_profile,
            text="Coach comment",
        )

        self.client.force_login(self.member_user)
        url = reverse(
            "food-post-comment-detail",
            kwargs={"post_id": self.food_post.id, "comment_id": comment.id},
        )

        data = {
            "text": "Trying to modify",
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("only modify your own comments", response.data["error"])

        # Verify comment unchanged
        comment.refresh_from_db()
        self.assertEqual(comment.text, "Coach comment")

    def test_delete_own_comment(self):
        """User can delete their own comment"""
        comment = FoodPostComment.objects.create(
            food_post=self.food_post,
            author=self.member_profile,
            text="Delete me",
        )

        self.client.force_login(self.member_user)
        url = reverse(
            "food-post-comment-detail",
            kwargs={"post_id": self.food_post.id, "comment_id": comment.id},
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(FoodPostComment.objects.filter(id=comment.id).exists())

    def test_cannot_delete_others_comment(self):
        """User cannot delete someone else's comment"""
        comment = FoodPostComment.objects.create(
            food_post=self.food_post,
            author=self.coach_profile,
            text="Coach feedback",
        )

        self.client.force_login(self.member_user)
        url = reverse(
            "food-post-comment-detail",
            kwargs={"post_id": self.food_post.id, "comment_id": comment.id},
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(FoodPostComment.objects.filter(id=comment.id).exists())

    def test_uncommented_food_posts_for_coach(self):
        """Coach can see food posts that need feedback"""
        # Create posts with and without comments
        FoodPostComment.objects.create(
            food_post=self.food_post,
            author=self.coach_profile,
            text="Already commented",
        )

        FoodPost.objects.create(
            user_profile=self.member_profile,
            coach=self.coach_profile,
            title="Needs Feedback",
            content="Lunch details",
        )

        self.client.force_login(self.coach_user)
        url = reverse("uncommented-food-posts")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["posts"][0]["title"], "Needs Feedback")

    def test_uncommented_posts_only_accessible_by_coach(self):
        """Only coaches can access uncommented posts endpoint"""
        self.client.force_login(self.member_user)
        url = reverse("uncommented-food-posts")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("Only coaches", response.data["error"])

    def test_comment_requires_authentication(self):
        """Anonymous users cannot comment"""
        url = reverse("food-post-comments", kwargs={"post_id": self.food_post.id})
        data = {"text": "Anonymous comment"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_multiple_comments_on_same_post(self):
        """Multiple users can comment on the same post"""
        self.client.force_login(self.member_user)
        url = reverse("food-post-comments", kwargs={"post_id": self.food_post.id})

        # Member comments
        response1 = self.client.post(url, {"text": "Member comment"}, format="json")
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Coach comments
        self.client.force_login(self.coach_user)
        response2 = self.client.post(url, {"text": "Coach comment"}, format="json")
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        # Should have 2 comments
        self.assertEqual(
            FoodPostComment.objects.filter(food_post=self.food_post).count(), 2
        )

    def test_comment_on_nonexistent_post(self):
        """Cannot comment on non-existent post"""
        self.client.force_login(self.member_user)
        url = reverse("food-post-comments", kwargs={"post_id": 99999})

        data = {"text": "Comment on nothing"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_coach_pending_relationship_cannot_comment(self):
        """Coach with pending relationship cannot comment"""
        # Change relationship to pending
        self.relationship.status = "pending"
        self.relationship.save()

        self.client.force_login(self.coach_user)
        url = reverse("food-post-comments", kwargs={"post_id": self.food_post.id})

        data = {"text": "Pending coach comment"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("not the assigned coach", response.data["error"])
