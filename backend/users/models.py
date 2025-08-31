from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_ROLES = [
        ('user', 'Normal User'),
        ('coach', 'Coach'),
        ('member', 'Member'),
    ]
    
    GOALS = [
        ('weight_loss', 'Weight Loss'),
        ('build_muscle', 'Build Muscle'),
        ('maintain_health', 'Maintain Health'),
    ]
    
    role = models.CharField(max_length=20, choices=USER_ROLES, default='user')
    goal = models.CharField(max_length=20, choices=GOALS, blank=True)

    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)  # in cm
    weight = models.FloatField(null=True, blank=True)  # in kg
    
    is_onboarding_complete = models.BooleanField(default=False)
    is_role_selected = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        role_display = self.get_role_display() if self.role else 'No Role'
        return f"{self.username} ({role_display})"