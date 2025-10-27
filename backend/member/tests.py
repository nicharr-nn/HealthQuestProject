# Create your tests here.
# from django.test import TestCase
# from .models import FoodPost
# from django.contrib.auth.models import User
# from coach.models import Coach
# from rest_framework.test import APIClient
# from django.contrib.auth import get_user_model
# #from .models import CoachMemberRealtionship

# User = get_user_model()

# class FoodPostTests(TestCase):
#     def setUp(self):

#         self.client = APIClient()
#         # Create dummy member for testing foodpost creation
#         self.user = User.objects.create_user(
#             username="member", password="pass123", email="member@example.com"
#         )
#         self.profile = self.user.userprofile
#         self.profile.role = "member"
#         self.profile.save()

#         # Create a dummy coach (required for comment foodpost)
#         self.coach_user = User.objects.create_user(username="coach"
#                          , password="coachpass", email="coach@example.com")
#         self.coach_profile = self.coach_user.userprofile
#         self.coach_profile.role = "coach"
#         self.coach_profile.save()

#         CoachMemberRealtionship.objects.create(
#             coach=self.coach_profile,  # if coach_profile is a UserProfile
#             user=self.profile,
#             status="active"
#        )

#         # Create a dummy food post
#         self.foodpost = FoodPost.objects.create(
#             title="Test Post",
#             content="This is a test food post.",
#             user_profile=self.profile,
#             coach=self.coach_profile
#         )
#         self.foodpost.user_profile = self.profile
#         self.foodpost.coach = self.coach_profile
#         self.foodpost.save()

#         # Log in as member user
#         self.client.force_login(self.user)


#     def test_food_post_creation(self):
#         """Test creating a food post invalid as normal user"""
#         url = "/api/foodpost/"
#         normal_user = User.objects.create_user(username="normaluser",
# password="normalpass", email="normaluser@example.com"
#         )
#         normal_profile = normal_user.userprofile
#         normal_profile.role = "normal"
#         normal_profile.save()
#         self.client.force_login(normal_user)

#         data = {
#             "user_profile": normal_profile.id,
#             "title": "Healthy Salad",
#             "content": "This is a recipe for a healthy salad.",
#             "coach": self.coach_profile.id
#         }
#         response = self.client.post(url, data, format='json')
#         # Forbidden since normal user is not a coach or member
#         self.assertEqual(response.status_code, 403)
#         # Only the initial post exists
#         self.assertEqual(FoodPost.objects.count(), 1)

#     def test_food_post_update(self):
#         """Test updating a food post"""
#         url = f"/api/foodpost/{self.foodpost.id}/update/"
#         data = {
#             "title": "Updated Test Post",
#             "content": "This is an updated test food post."
#         }
#         response = self.client.put(url, data, format='json')
#         self.assertEqual(response.status_code, 200)
#         self.foodpost.refresh_from_db()
#         self.assertEqual(self.foodpost.title, "Updated Test Post")
#         self.assertEqual(self.foodpost.content, "This is an updated test food post.")
