from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    ROLE_CHOICES = [
        ("normal", "Normal User"),
        ("coach", "Coach"),
        ("member", "Member"),
        ("admin", "Administrator"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="normal")
    height = models.FloatField(null=True, blank=True)  # in cm
    weight = models.FloatField(null=True, blank=True)  # in kg
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True
    )
    location = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    def can_have_fitness_goals(self):
        """Check if this user can have fitness goals (only normal users can)"""
        return self.role == "normal"


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            UserProfile.objects.create(user=instance, role="admin")
        else:
            UserProfile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    # only save if it exists
    if hasattr(instance, "userprofile"):
        instance.userprofile.save()


# Connect signals after class definition
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)


class FitnessGoal(models.Model):
    GOAL_CHOICES = [
        ("lose_weight", "Lose Weight"),
        ("build_muscle", "Build Muscle"),
        ("improve_endurance", "Improve Endurance"),
        ("general_fitness", "General Fitness"),
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
