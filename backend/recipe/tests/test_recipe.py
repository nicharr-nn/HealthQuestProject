from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Recipe, RecipeRating


class RecipeTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()

        # Create coach user
        self.coach = User.objects.create_user(
            username="coachuser", password="coachpass", email="testcoach@example.com"
        )
        self.coach_profile = self.coach.userprofile
        self.coach_profile.role = "coach"
        self.coach_profile.save()

        # Create normal user (Bronze)
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

        # Create silver user
        self.silver_user = User.objects.create_user(
            username="silveruser", password="silverpass", email="silver@example.com"
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
            username="golduser", password="goldpass", email="gold@example.com"
        )
        self.gold_profile = self.gold_user.userprofile
        self.gold_profile.role = "normal"
        self.gold_level = self.gold_profile.get_current_level()
        if self.gold_level:
            self.gold_level.level = "Gold"
            self.gold_level.save()
        self.gold_profile.save()

        # Create test recipe
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            ingredients="Ingredient1, Ingredient2",
            steps="Step1, Step2",
            user_profile=self.coach_profile,
            access_level="all",
        )

    def test_recipe_list_unauthenticated(self):
        """Test that unauthenticated users cannot access recipes"""
        url = reverse("recipe-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_recipe_coach_access(self):
        """Test that coaches can access the recipe endpoint"""
        url = reverse("recipe-list")

        self.client.force_login(self.coach)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.client.logout()

    def test_recipe_bronze_access(self):
        """Test that users with bronze level can't access the recipe endpoint"""
        url = reverse("recipe-list")

        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_recipe_silver_access(self):
        """Test that users with silver level can access the recipe endpoint"""
        url = reverse("recipe-list")

        self.client.force_login(self.silver_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.client.logout()

    def test_recipe_gold_access(self):
        """Test that users with gold level can access the recipe endpoint"""
        url = reverse("recipe-list")

        self.client.force_login(self.gold_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.client.logout()

    def test_recipe_list_search(self):
        """Test searching recipes by title"""
        # Create additional recipes
        Recipe.objects.create(
            title="Chicken Salad",
            ingredients="Chicken, Lettuce",
            steps="Mix ingredients",
            user_profile=self.coach_profile,
        )
        Recipe.objects.create(
            title="Beef Stew",
            ingredients="Beef, Potatoes",
            steps="Cook ingredients",
            user_profile=self.coach_profile,
        )

        url = reverse("recipe-list")
        self.client.force_login(self.coach)

        # Search for "Salad"
        response = self.client.get(url, {"search": "Salad"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Chicken Salad")
        self.client.logout()

    def test_recipe_list_sort_newest(self):
        """Test sorting recipes by newest"""
        url = reverse("recipe-list")
        self.client.force_login(self.coach)

        response = self.client.get(url, {"sort_by": "newest"})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)
        self.client.logout()

    def test_recipe_list_sort_oldest(self):
        """Test sorting recipes by oldest"""
        url = reverse("recipe-list")
        self.client.force_login(self.coach)

        response = self.client.get(url, {"sort_by": "oldest"})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)
        self.client.logout()

    def test_recipe_list_sort_title_az(self):
        """Test sorting recipes by title A-Z"""
        url = reverse("recipe-list")
        self.client.force_login(self.coach)

        response = self.client.get(url, {"sort_by": "title_az"})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)
        self.client.logout()

    def test_recipe_list_sort_title_za(self):
        """Test sorting recipes by title Z-A"""
        url = reverse("recipe-list")
        self.client.force_login(self.coach)

        response = self.client.get(url, {"sort_by": "title_za"})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)
        self.client.logout()

    def test_recipe_list_filter_min_rating(self):
        """Test filtering recipes by minimum rating"""
        # Add ratings to the recipe
        RecipeRating.objects.create(
            recipe=self.recipe,
            user_profile=self.silver_profile,
            rating=4,
        )
        RecipeRating.objects.create(
            recipe=self.recipe,
            user_profile=self.gold_profile,
            rating=5,
        )

        url = reverse("recipe-list")
        self.client.force_login(self.coach)

        response = self.client.get(url, {"min_rating": "4"})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)
        self.client.logout()

    def test_coach_create_recipe(self):
        """Test that a coach can create a recipe"""
        url = reverse("recipe-list")

        self.client.force_login(self.coach)
        data = {
            "title": "Healthy Salad",
            "ingredients": "Lettuce, Tomato, Cucumber",
            "steps": "Mix all ingredients.",
            "access_level": "silver",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "Healthy Salad")
        self.assertTrue(Recipe.objects.filter(title="Healthy Salad").exists())
        self.client.logout()

    def test_gold_create_recipe(self):
        """Test that a gold user can create a recipe"""
        url = reverse("recipe-list")

        self.client.force_login(self.gold_user)
        data = {
            "title": "Overnight Oats",
            "ingredients": "Oats, Milk, Yogurt, Chia Seeds",
            "steps": "Combine all ingredients in a jar and refrigerate overnight.",
            "access_level": "gold",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "Overnight Oats")
        self.client.logout()

    def test_bronze_cannot_create_recipe(self):
        """Test that bronze users cannot create recipes"""
        url = reverse("recipe-list")

        self.client.force_login(self.user)
        data = {
            "title": "Unauthorized Recipe",
            "ingredients": "Test",
            "steps": "Test",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_silver_cannot_create_recipe(self):
        """Test that silver users cannot create recipes"""
        url = reverse("recipe-list")

        self.client.force_login(self.silver_user)
        data = {
            "title": "Unauthorized Recipe",
            "ingredients": "Test",
            "steps": "Test",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_recipe_detail(self):
        """Test retrieving a single recipe"""
        url = reverse("recipe-detail", kwargs={"pk": self.recipe.pk})

        self.client.force_login(self.coach)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.recipe.id)
        self.assertEqual(response.data["title"], "Test Recipe")
        self.client.logout()

    def test_recipe_detail_not_found(self):
        """Test retrieving a non-existent recipe"""
        url = reverse("recipe-detail", kwargs={"pk": 99999})

        self.client.force_login(self.coach)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_my_recipes(self):
        """Test retrieving only user's own recipes"""
        # Create recipes for different users
        Recipe.objects.create(
            title="Coach Recipe 2",
            ingredients="Test",
            steps="Test",
            user_profile=self.coach_profile,
        )
        Recipe.objects.create(
            title="Gold Recipe",
            ingredients="Test",
            steps="Test",
            user_profile=self.gold_profile,
        )

        url = reverse("my-recipes")

        self.client.force_login(self.coach)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Coach should have 2 recipes (from setUp + one created here)
        self.assertEqual(len(response.data), 2)
        for recipe in response.data:
            self.assertEqual(recipe["user_profile"], "coachuser - coach")
        self.client.logout()

    def test_my_recipes_with_sorting(self):
        """Test retrieving user's recipes with sorting"""
        url = reverse("my-recipes")

        self.client.force_login(self.coach)
        response = self.client.get(url, {"sort_by": "title_az"})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)
        self.client.logout()

    def test_edit_recipe_as_owner(self):
        """Test that a user can edit their own recipe"""
        url = reverse("recipe-list")

        self.client.force_login(self.coach)
        data = {
            "title": "Salmon Salad",
            "ingredients": "Salmon, Lettuce, Tomato, Cucumber",
            "steps": "Combine all ingredients in a bowl and toss.",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        recipe_id = response.data.get("id")

        # Edit the recipe using PUT
        edit_url = reverse("update-recipe", kwargs={"id": recipe_id})
        edit_data = {
            "title": "Updated Salmon Salad",
            "ingredients": "Salmon, Lettuce, Tomato, Cucumber, Avocado",
            "steps": "Combine all ingredients in a bowl and toss well.",
        }
        edit_response = self.client.put(edit_url, edit_data, format="json")
        self.assertEqual(edit_response.status_code, 200)
        self.assertEqual(edit_response.data["success"], True)
        self.assertEqual(edit_response.data["recipe"]["title"], "Updated Salmon Salad")
        self.client.logout()

    def test_edit_recipe_patch(self):
        """Test partial update of recipe using PATCH"""
        url = reverse("update-recipe", kwargs={"id": self.recipe.id})

        self.client.force_login(self.coach)
        data = {
            "title": "Partially Updated Recipe",
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(response.data["recipe"]["title"], "Partially Updated Recipe")
        self.client.logout()

    def test_edit_recipe_unauthorized(self):
        """Test that a user cannot edit someone else's recipe"""
        url = reverse("recipe-list")

        self.client.force_login(self.coach)
        data = {
            "title": "Chicken Salad",
            "ingredients": "Chicken, Lettuce, Tomato, Cucumber",
            "steps": "Combine all ingredients in a bowl and toss.",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        recipe_id = response.data.get("id")
        self.client.logout()

        # Attempt to edit the recipe as silver user
        self.client.force_login(self.silver_user)
        edit_url = reverse("update-recipe", kwargs={"id": recipe_id})
        edit_data = {
            "title": "Malicious Edit",
            "ingredients": "Hacked Ingredients",
            "steps": "Hacked Steps.",
        }
        edit_response = self.client.put(edit_url, edit_data, format="json")
        self.assertEqual(edit_response.status_code, 403)
        self.client.logout()

    def test_delete_recipe_as_owner(self):
        """Test that a user can delete their own recipe"""
        # Create a recipe to delete
        recipe_to_delete = Recipe.objects.create(
            title="Recipe to Delete",
            ingredients="Test",
            steps="Test",
            user_profile=self.coach_profile,
        )

        url = reverse("delete-recipe", kwargs={"id": recipe_to_delete.id})

        self.client.force_login(self.coach)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Recipe.objects.filter(id=recipe_to_delete.id).exists())
        self.client.logout()

    def test_delete_recipe_unauthorized(self):
        """Test that a user cannot delete someone else's recipe"""
        url = reverse("delete-recipe", kwargs={"id": self.recipe.id})

        self.client.force_login(self.silver_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Recipe.objects.filter(id=self.recipe.id).exists())
        self.client.logout()

    def test_upload_recipe_image(self):
        """Test uploading an image to a recipe"""
        url = reverse("upload-recipe-image", kwargs={"id": self.recipe.id})

        # Create a simple test image
        image = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )

        self.client.force_login(self.coach)
        response = self.client.post(url, {"image": image}, format="multipart")
        self.assertEqual(response.status_code, 200)
        self.assertIn("photo_url", response.data)
        self.recipe.refresh_from_db()
        self.assertTrue(bool(self.recipe.image))
        self.client.logout()

    def test_upload_recipe_image_no_file(self):
        """Test uploading without providing an image file"""
        url = reverse("upload-recipe-image", kwargs={"id": self.recipe.id})

        self.client.force_login(self.coach)
        response = self.client.post(url, {}, format="multipart")
        self.assertEqual(response.status_code, 400)
        self.assertIn("No image file provided", response.data["detail"])
        self.client.logout()

    def test_upload_recipe_image_unauthorized(self):
        """Test that a user cannot upload image to someone else's recipe"""
        url = reverse("upload-recipe-image", kwargs={"id": self.recipe.id})

        image = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )

        self.client.force_login(self.silver_user)
        response = self.client.post(url, {"image": image}, format="multipart")
        self.assertEqual(response.status_code, 403)
        self.client.logout()


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
                recipe=self.recipe, user_profile=self.silver_profile
            ).exists()
        )
        self.client.logout()

    def test_give_rating_update(self):
        """Test updating an existing rating"""
        # Create initial rating
        RecipeRating.objects.create(
            recipe=self.recipe, user_profile=self.silver_profile, rating=3
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
            recipe=self.recipe, user_profile=self.silver_profile
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
            recipe=self.recipe, user_profile=self.silver_profile, rating=4
        )
        RecipeRating.objects.create(
            recipe=self.recipe, user_profile=self.gold_profile, rating=5
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
            recipe=self.recipe, user_profile=self.silver_profile, rating=4
        )

        url = reverse("delete-recipe-rating", kwargs={"id": self.recipe.id})

        self.client.force_login(self.silver_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            RecipeRating.objects.filter(
                recipe=self.recipe, user_profile=self.silver_profile
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
            access_level="gold",
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
# Run specific test: python manage.py test recipe.RecipeTests.test_recipe_coach_access
