from django.test import TestCase
from django.contrib.auth import get_user_model
from app.models import UserProfile, WorkoutCompletion, WorkoutAssignment

User = get_user_model()

class UserCascadeDeleteTest(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create(
            username="testuser",
            email="test@example.com"
        )

        # Create related UserProfile
        self.profile = UserProfile.objects.create(
            user=self.user,
            age=25,
            gender="Male",
            location="NYC"
        )

        # Create WorkoutCompletion
        self.workout_completion = WorkoutCompletion.objects.create(
            user=self.user,
            xp_earned=100
        )

        # Create WorkoutAssignment
        self.workout_assignment = WorkoutAssignment.objects.create(
            user=self.user,
            status="pending"
        )

    def test_user_cascade_delete(self):
        # Delete user
        self.user.delete()

        # Assert all related records are deleted
        self.assertFalse(User.objects.filter(id=self.user.id).exists())
        self.assertFalse(UserProfile.objects.filter(user_id=self.user.id).exists())
        self.assertFalse(WorkoutCompletion.objects.filter(user_id=self.user.id).exists())
        self.assertFalse(WorkoutAssignment.objects.filter(user_id=self.user.id).exists())
