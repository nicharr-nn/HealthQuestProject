from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Recipe, RecipeRating
from django.conf import settings

class RecipeRatingTests(TestCase):
    def setUp(self):
        """Set up test data for rating tests"""
        self.client = APIClient()

        # Create coach
        self.coach = User.objects.create_user(
            username="coach", password="pass", email="coach@test.com"
        )
        self.coach_profile = self.coach.userprofile
        self.coach_profile.role = "coach"
        self.coach_profile.save()

        # Create silver user
        self.silver_user = User.objects.create_user(
            username="silver", password="pass", email="silver@test.com"
        )
        self.silver_profile = self.silver_user.userprofile
        self.silver_profile.role = "normal"
        self.silver_level = self.silver_profile.get_current_level()
        if self.silver_level:
            self.silver_level.level = "Silver"
            self.silver_level.save()
        self.silver_profile.save()

        # Create gold user
        self.gold_user = User.objects.create_user(
            username="gold", password="pass", email="gold@test.com"
        )
        self.gold_profile = self.gold_user.userprofile
        self.gold_profile.role = "normal"
        self.gold_level = self.gold_profile.get_current_level()
        if self.gold_level:
            self.gold_level.level = "Gold"
            self.gold_level.save()
        self.gold_profile.save()

        # Create recipe
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            ingredients="Test",
            steps="Test",
            user_profile=self.coach_profile,
        )

    def test_give_rating_create(self):
        """Test creating a new rating"""
        url = reverse("give-recipe-rating", kwargs={"id": self.recipe.id})

        self.client.force_login(self.silver_user)
        data = {"rating": 5}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["rating"], 5)
        self.assertTrue(response.data["created"])
        self.assertTrue(
            RecipeRating.objects.filter(
                recipe=self.recipe,
                user_profile=self.silver_profile
            ).exists()
        )
        self.client.logout()

    def test_give_rating_update(self):
        """Test updating an existing rating"""
        # Create initial rating
        RecipeRating.objects.create(
            recipe=self.recipe,
            user_profile=self.silver_profile,
            rating=3
        )

        url = reverse("give-recipe-rating", kwargs={"id": self.recipe.id})

        self.client.force_login(self.silver_user)
        data = {"rating": 5}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["rating"], 5)
        self.assertFalse(response.data["created"])
        
        # Verify update
        rating = RecipeRating.objects.get(
            recipe=self.recipe,
            user_profile=self.silver_profile
        )
        self.assertEqual(rating.rating, 5)
        self.client.logout()

    def test_give_rating_invalid_value(self):
        """Test rating with invalid value"""
        url = reverse("give-recipe-rating", kwargs={"id": self.recipe.id})

        self.client.force_login(self.silver_user)
        
        # Test rating outside range
        data = {"rating": 6}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        
        # Test rating = 0
        data = {"rating": 0}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        
        self.client.logout()

    def test_give_rating_no_value(self):
        """Test rating without providing a rating value"""
        url = reverse("give-recipe-rating", kwargs={"id": self.recipe.id})

        self.client.force_login(self.silver_user)
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Rating value required", response.data["detail"])
        self.client.logout()

    def test_give_rating_own_recipe(self):
        """Test that user cannot rate their own recipe"""
        url = reverse("give-recipe-rating", kwargs={"id": self.recipe.id})

        self.client.force_login(self.coach)
        data = {"rating": 5}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("cannot rate your own recipe", response.data["detail"])
        self.client.logout()

    def test_get_rating(self):
        """Test retrieving recipe ratings"""
        # Create some ratings
        RecipeRating.objects.create(
            recipe=self.recipe,
            user_profile=self.silver_profile,
            rating=4
        )
        RecipeRating.objects.create(
            recipe=self.recipe,
            user_profile=self.gold_profile,
            rating=5
        )

        url = reverse("get-recipe-rating", kwargs={"id": self.recipe.id})

        self.client.force_login(self.coach)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["recipe_id"], self.recipe.id)
        self.assertEqual(response.data["rating_count"], 2)
        self.assertEqual(response.data["average_rating"], 4.5)
        self.assertEqual(len(response.data["ratings"]), 2)
        self.client.logout()

    def test_delete_rating(self):
        """Test deleting a rating"""
        # Create rating
        RecipeRating.objects.create(
            recipe=self.recipe,
            user_profile=self.silver_profile,
            rating=4
        )

        url = reverse("delete-recipe-rating", kwargs={"id": self.recipe.id})

        self.client.force_login(self.silver_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            RecipeRating.objects.filter(
                recipe=self.recipe,
                user_profile=self.silver_profile
            ).exists()
        )
        self.client.logout()

    def test_delete_rating_not_found(self):
        """Test deleting a rating that doesn't exist"""
        url = reverse("delete-recipe-rating", kwargs={"id": self.recipe.id})

        self.client.force_login(self.silver_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_download_recipe_pdf(self):
        """Test downloading recipe PDF"""
        url = reverse("download-recipe-pdf", kwargs={"id": self.recipe.id})

        self.client.force_login(self.coach)
        response = self.client.get(url)
        # PDF generation might create the file or return 200
        self.assertIn(response.status_code, [200, 201])
        self.client.logout()

    def test_download_recipe_pdf_gold_access(self):
        """Test downloading gold-level recipe PDF"""
        # Create gold-level recipe
        gold_recipe = Recipe.objects.create(
            title="Gold Recipe",
            ingredients="Premium ingredients",
            steps="Premium steps",
            user_profile=self.coach_profile,
            access_level="gold"
        )

        url = reverse("download-recipe-pdf", kwargs={"id": gold_recipe.id})

        # Silver user should not have access
        self.client.force_login(self.silver_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        # Gold user should have access
        self.client.force_login(self.gold_user)
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 201])
        self.client.logout()


# Run the tests with: python manage.py test recipe
# Run specific test: python manage.py test recipe.RecipeRatingTests