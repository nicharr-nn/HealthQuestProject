from django.db import models

from users.models import UserProfile
from member.models import Member
from django.utils import timezone


class WorkoutProgram(models.Model):
    CATEGORY_CHOICES = [
        ("strength_training", "Strength Training"),
        ("cardio", "Cardio"),
        ("weight_loss", "Weight Loss"),
        ("muscle_building", "Muscle Building"),
        ("endurance", "Endurance"),
        ("flexibility", "Flexibility"),
        ("full_body", "Full Body"),
    ]

    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    coach = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="programs",
        limit_choices_to={"role": "coach"},
        db_column="coach_id",  # explicit DB column
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    level_access = models.CharField(max_length=50, default="all")
    difficulty_level = models.CharField(
        max_length=50, choices=DIFFICULTY_CHOICES, default="easy"
    )
    is_public = models.BooleanField(default=True)
    duration = models.IntegerField(help_text="Total duration in days", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default="full_body"
    )

    def __str__(self):
        return f"{self.title} (Coach: {self.coach.user.username})"


class WorkoutDay(models.Model):
    WORKOUT_TYPE_CHOICES = [
        ("strength_training", "Strength Training"),
        ("cardio", "Cardio"),
        ("hiit", "HIIT"),
        ("flexibility", "Flexibility"),
        ("recovery", "Recovery"),
        ("full_body", "Full Body"),
        ("upper_body", "Upper Body"),
        ("lower_body", "Lower Body"),
        ("core", "Core"),
    ]

    program = models.ForeignKey(
        WorkoutProgram,
        on_delete=models.CASCADE,
        related_name="days",
        db_column="program_id",
    )
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255, blank=True, null=True)
    video_links = models.JSONField(default=list)  # store multiple links as list
    duration = models.IntegerField(default=30)  # minutes total
    completed_by = models.ManyToManyField(
        UserProfile,
        through="WorkoutDayCompletion",
        related_name="completed_days",
    )
    type = models.CharField(
        max_length=50,
        choices=WORKOUT_TYPE_CHOICES,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["day_number"]

    def __str__(self):
        return f"{self.program.title} - Day {self.day_number}"


class WorkoutDayCompletion(models.Model):
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        db_column="user_profile_id",
    )
    workout_day = models.ForeignKey(
        WorkoutDay,
        on_delete=models.CASCADE,
        db_column="workout_day_id",
    )
    completed_at = models.DateTimeField(auto_now_add=True)
    xp_earned = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user_profile", "workout_day")


class WorkoutAssignment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("paused", "Paused"),
        ("overdue", "Overdue"),
    ]

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="assignments",
        null=True,  # removed after testing
        blank=True,  # removed after testing
    )

    program = models.ForeignKey(
        WorkoutProgram,
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    assigned_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    completed_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-assigned_date"]
        unique_together = ("member", "program")

    def __str__(self):
        return f"{self.member.user.user.username} → {self.program.title}"

    def check_completion(self):
        """Check if all day_numbers are completed."""
        total_days = self.program.days.values("day_number").distinct().count()
        completed_days = (
            WorkoutDayCompletion.objects.filter(
                user_profile=self.member.user, workout_day__program=self.program
            )
            .values("workout_day__day_number")
            .distinct()
            .count()
        )

        if completed_days >= total_days:
            self.status = "completed"
            self.completed_date = timezone.now().date()
            self.save(update_fields=["status", "completed_date"])
            return True
        return False
