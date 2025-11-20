from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from recipe.models import Recipe
from member.models import UserProfile


class RecipeViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # User
        self.user = User.objects.create_user(
            username="user1", password="pass1"
        )
        self.user_profile = self.user.userprofile

        # Recipe created by user
        self.recipe = Recipe.objects.create(
            user_profile=self.user_profile,
            title="Test Recipe",
        )

    def test_user_can_delete_own_recipe(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("delete_recipe", kwargs={"recipe_id": self.recipe.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Recipe.objects.filter(pk=self.recipe.pk).exists())

    def test_user_cannot_delete_others_recipe(self):
        other_user = User.objects.create_user(username="user2", password="pass2")
        self.client.force_authenticate(user=other_user)
        url = reverse("delete_recipe", kwargs={"recipe_id": self.recipe.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
