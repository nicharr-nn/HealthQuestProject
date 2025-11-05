from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
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

    LOCATION_CHOICES = [
        ("TH", "Thailand"),
        ("USA", "United States"),
        ("UK", "United Kingdom"),
        ("JP", "Japan"),
        ("LA", "Laos"),
        ("KR", "South Korea"),
        ("O", "Other"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    height = models.FloatField(null=True, blank=True)  # in cm
    weight = models.FloatField(null=True, blank=True)  # in kg
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True
    )
    location = models.CharField(
        max_length=100, choices=LOCATION_CHOICES, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    def can_have_fitness_goals(self):
        """Check if this user can have fitness goals (only normal users can)"""
        return self.role == "normal" or self.role == "member"

    def get_current_level(self):
        """
        Return the most recent UserLevel row (current) or create default one.
        """
        ul = self.user_levels.order_by("-level_rank").first()
        if not ul:
            # create default Bronze level row
            ul = UserLevel.objects.create(
                user_profile=self, level="Bronze", level_rank=1, xp=0
            )
        return ul


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
                "Only users with 'normal' and member role can have fitness goals."
            )

    def save(self, *args, **kwargs):
        """Override save to enforce validation"""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.goal_type}"


class UserLevel(models.Model):
    level = models.CharField(max_length=20)
    level_rank = models.IntegerField(default=1)
    user_profile = models.ForeignKey(
        "UserProfile", on_delete=models.CASCADE, related_name="user_levels"
    )
    xp = models.IntegerField(default=0)
    goal_achieved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.level} (xp={self.xp})"

    def add_xp(self, amount: int):
        """
        Increase xp by `amount`, recompute level, and save.
        Returns a tuple: (leveled_up: bool, previous_level_rank, new_level_rank)
        """
        from workout.xp_rules import level_for_xp

        amount = int(amount or 0)
        if amount <= 0:
            return (False, self.level_rank, self.level_rank)

        previous_rank = self.level_rank
        self.xp = max(0, self.xp + amount)

        new_rank, new_name, xp_needed = level_for_xp(self.xp)
        self.level_rank = new_rank
        self.level = new_name
        self.save()
        
        # Check goal achievement after level up
        self.check_goal_achievement()
        
        return (new_rank != previous_rank, previous_rank, new_rank)

    def check_goal_achievement(self):
        """
        Check if user has achieved their fitness goals based on current stats
        """
        from workout.models import WorkoutDayCompletion
        
        try:
            active_goals = self.user_profile.fitness_goals.filter(
                end_date__isnull=True  # Ongoing goals
            )
            
            if not active_goals.exists():
                self.goal_achieved = False
                self.save(update_fields=["goal_achieved"])
                return False
            
            goal_achieved = False
            for goal in active_goals:
                if self._meets_goal_criteria(goal):
                    goal_achieved = True
                    break
            
            if self.goal_achieved != goal_achieved:
                self.goal_achieved = goal_achieved
                self.save(update_fields=["goal_achieved"])
            
            return goal_achieved
            
        except Exception as e:
            print(f"Error in check_goal_achievement: {e}")
            return False

    def meets_goal_criteria(self, goal):
        """
        Check if this user level meets specific goal criteria
        """
        from workout.models import WorkoutDayCompletion
        completed_workouts = WorkoutDayCompletion.objects.filter(
                user_profile=self.user_profile
            ).count()
        
        if goal.goal_type == "lose_weight":
            return completed_workouts >= 5
        
        elif goal.goal_type == "build_muscle":
            return completed_workouts >= 10
        
        elif goal.goal_type == "improve_endurance":
            total_duration = WorkoutDayCompletion.objects.filter(
                user_profile=self.user_profile
            ).aggregate(
                total_duration=models.Sum('workout_day__duration')
            )['total_duration'] or 0
            return total_duration >= 500
        
        elif goal.goal_type == "general_fitness":
            return self.level_rank >= 1 and completed_workouts >= 5
        
        elif goal.goal_type == "increase_flexibility":
            return completed_workouts >= 15
        
        return False


class Achievement(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    xp_reward = models.IntegerField(default=0)
    level_required = models.IntegerField(default=1)  # minimum level_rank required

    def __str__(self):
        return f"{self.title} - Level {self.level_required} - {self.xp_reward} XP"


class UserAchievement(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="achievements"
    )
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_earned = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.achievement.title}"
