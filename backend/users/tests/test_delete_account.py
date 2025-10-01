from django.test import TestCase
from django.contrib.auth import get_user_model
from django.apps import apps
from rest_framework.test import APIClient

User = get_user_model()

def get_user_profile_model():
    return apps.get_model("users", "UserProfile")

class UserDeletionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com", 
            password="testpass123"
        )
        self.UserProfile = get_user_profile_model()
        
        # FIX: Use get_or_create to avoid duplicates
        self.profile, created = self.UserProfile.objects.get_or_create(
            user=self.user,
            defaults={
                'age': 25,
                'gender': "M",
                'location': "UK"
            }
        )

    def test_user_deactivation_via_api(self):
        """Test the actual DELETE endpoint behavior"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(f'/api/user/{self.user.id}/')
        
        # Check response
        if response.status_code != 200:
            print(f"Response status: {response.status_code}")
            print(f"Response data: {response.data}")
        
        self.assertEqual(response.status_code, 200)
        
        # User should be deactivated but not deleted
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        
        # Profile should still exist
        self.assertTrue(self.UserProfile.objects.filter(user=self.user).exists())

    def test_cannot_delete_other_users(self):
        """Test users can only delete their own account"""
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="otherpass123"
        )
        
        # Create profile for other user
        self.UserProfile.objects.get_or_create(
            user=other_user,
            defaults={'age': 30, 'gender': 'F', 'location': 'O'}
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/user/{other_user.id}/')
        
        self.assertEqual(response.status_code, 403)

    def test_unauthenticated_cannot_delete(self):
        """Test that unauthenticated requests are rejected"""
        response = self.client.delete(f'/api/user/{self.user.id}/')
        self.assertIn(response.status_code, [401,403])

# To run the tests, use the command:
# python manage.py test backend.users.tests.test_delete_account