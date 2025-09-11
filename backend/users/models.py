from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_ROLES = [
        ('user', 'Normal User'),
        ('coach', 'Coach'),
        ('member', 'Member'),
    ]

    # GOAL_CHOICES = [
    #     ('WEIGHT_LOSS', 'Weight Loss'),
    #     ('MUSCLE_GAIN', 'Muscle Gain'), 
    #     ('MAINTENANCE', 'Maintenance'),
    # ]
    
    role = models.CharField(max_length=20, choices=USER_ROLES, default='user')
    # goal = models.CharField(max_length=20, choices=GOAL_CHOICES, blank=True)

    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)  # in cm
    weight = models.FloatField(null=True, blank=True)  # in kg

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # role_display = self.get_role_display() if self.role else 'No Role'
        # return f"{self.username} ({role_display})"
        return self.email or self.username
    
    # def clean(self):
    #     if self.goal and self.goal not in dict(self.GOAL_CHOICES):
    #         raise ValidationError({'goal': 'Invalid goal selection'})