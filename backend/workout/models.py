from django.db.models.signals import post_save
from django.db import models
from users.models import UserProfile
from django.utils import timezone


class WorkoutProgram(models.Model):
    coach = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="programs",
        limit_choices_to={"role": "coach"},
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    level_access = models.CharField(max_length=50, default="all")  
    difficulty_level = models.CharField(max_length=50, default="easy")
    is_public = models.BooleanField(default=True)
    duration = models.IntegerField(help_text="Total duration in days", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} (Coach: {self.coach.user.username})"


class WorkoutDay(models.Model):
    program = models.ForeignKey(
        WorkoutProgram, on_delete=models.CASCADE, related_name="days"
    )
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255, blank=True, null=True)
    video_links = models.JSONField(default=list)  # store multiple links as list
    duration = models.IntegerField(default=30)  # minutes total
    completed_by = models.ManyToManyField(
        UserProfile, through="WorkoutDayCompletion", related_name="completed_days"
    )

    class Meta:
        unique_together = ("program", "day_number")
        ordering = ["day_number"]

    def __str__(self):
        return f"{self.program.title} - Day {self.day_number}"


class WorkoutDayCompletion(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    workout_day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    xp_earned = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user_profile", "workout_day")

    
class WorkoutAssignment(models.Model):
    user_profile = models.ForeignKey(
        "users.UserProfile", on_delete=models.CASCADE, related_name="assignments"
    )
    program = models.ForeignKey("WorkoutProgram", on_delete=models.CASCADE)
    assigned_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default="pending")
    completed_date = models.DateField(null=True, blank=True)

    def check_completion(self):
        """Check if all days in the program are completed by this user"""
        total_days = self.program.days.count()
        completed_days = self.user_profile.completed_days.filter(program=self.program).count()

        if completed_days >= total_days and total_days > 0:
            self.status = "completed"
            self.completed_date = timezone.now().date()
            self.save(update_fields=["status", "completed_date"])
            return True
        return False


