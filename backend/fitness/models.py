from django.db import models
from django.core.exceptions import ValidationError
from django.apps import apps
from users.models import UserProfile

class FitnessGoal(models.Model):
    GOAL_CHOICES = [
        ("lose_weight", "Lose Weight"),
        ("build_muscle", "Build Muscle"),
        ("improve_endurance", "Improve Endurance"),
        ("general_fitness", "General Fitness"),
        ("increase_flexibility", "Increase Flexibility"),
    ]

    goal_type = models.CharField(
        max_length=255, choices=GOAL_CHOICES, null=True, blank=True
    )
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="fitness_goals"
    )

    def clean(self):
        """Validate that only normal users can have fitness goals"""
        super().clean()
        if not self.user_profile.can_have_fitness_goals():
            raise ValidationError(
                "Only users with 'normal' role can have fitness goals."
            )

    def save(self, *args, **kwargs):
        """Override save to enforce validation"""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.goal_type}"
    
