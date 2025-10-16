from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Recipe


class RecipeTests(TestCase):
    def setUp(self):
        
        self.client = APIClient()
        self.coach = User.objects.create_user(
            username="coachuser", password="coachpass", email="testcoach@example.com"
        )
        self.coach_profile = self.coach.userprofile
        self.coach_profile.role = "coach"
        self.coach_profile.save()

        self.user = User.objects.create_user(
            username="normaluser", password="normalpass", email="normaluser@example.com"
        )
        self.user_profile = self.user.userprofile
        self.user_profile.role = "normal"
        self.user_level = self.user_profile.get_current_level()
        if self.user_level:
            self.user_level.level = "Bronze"
            self.user_level.save()
        self.user_profile.save()

        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            ingredients="Ingredient1, Ingredient2",
            steps="Step1, Step2",
            user_profile=self.coach_profile
        )

    def test_recipe_coach_access(self):
        """Test that coaches can access the recipe endpoint"""
        url = "/api/recipe/"

        # Test as unauthenticated user
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Test as coach user
        self.client.force_login(self.coach)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Success
        self.client.logout()

    def test_recipe_bronze_access(self):
        """Test that users with bronze level can't access the recipe endpoint"""
        url = "/api/recipe/"

        # Test as unauthenticated user
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Test as bronze user
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Forbidden
        self.client.logout()

    def test_recipe_silver_access(self):
        """Test that users with silver level can access the recipe endpoint"""
        url = "/api/recipe/"

        # Upgrade user to silver level
        if self.user_level:
            self.user_level.level = "Silver"
            self.user_level.save()

        # Test as silver user
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Success
        self.client.logout()

    def test_recipe_gold_access(self):
        """Test that users with gold level can access the recipe endpoint"""
        url = "/api/recipe/"

        # Upgrade user to gold level
        if self.user_level:
            self.user_level.level = "Gold"
            self.user_level.save()

        # Test as gold user
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Success
        self.client.logout()
    
    def test_coach_create_recipe(self):
        """Test that a coach can create a recipe"""
        url = "/api/recipe/"

        self.client.force_login(self.coach)
        data = {
            "title": "Healthy Salad",
            "ingredients": "Lettuce, Tomato, Cucumber",
            "steps": "Mix all ingredients.",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.client.logout()
    
    def test_gold_create_recipe(self):
        """Test that a gold user can create a recipe"""
        url = "/api/recipe/"

        # Upgrade user to gold level
        if self.user_level:
            self.user_level.level = "Gold"
            self.user_level.save()

        self.client.force_login(self.user)
        data = {
            "title": "Overnight Oats",
            "ingredients": "Oats, Milk, Yogurt, Chia Seeds",
            "steps": "Combine all ingredients in a jar and refrigerate overnight.",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.client.logout()
    
    def test_edit_recipe(self):
        """Test that a user can edit their own recipe"""

        url = "/api/recipe/"

        self.client.force_login(self.coach)
        data = {
            "title": "Salmon Salad",
            "ingredients": "Salmon, Lettuce, Tomato, Cucumber",
            "steps": "Combine all ingredients in a bowl and toss.",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        recipe_id = response.data.get("id")

        # Edit the recipe
        edit_url = f"/api/recipe/{recipe_id}/update/"
        edit_data = {
            "title": "Updated Salmon Salad",
            "ingredients": "Salmon, Lettuce, Tomato, Cucumber, Avocado",
            "steps": "Combine all ingredients in a bowl and toss. Add avocado for creaminess.",
        }
        edit_response = self.client.put(edit_url, edit_data, format='json')
        self.assertEqual(edit_response.status_code, 200)
        self.assertEqual(edit_response.data['success'], True)
        self.client.logout()
