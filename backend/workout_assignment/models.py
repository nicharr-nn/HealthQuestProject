from django.db import models
from django.utils import timezone
from users.models import UserProfile
from workout.models import WorkoutProgram


class WorkoutAssignment(models.Model):
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="assignments",
        db_column="user_profile_id",
    )
    program = models.ForeignKey(
        WorkoutProgram,
        on_delete=models.CASCADE,
        db_column="program_id",
    )
    assigned_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default="pending")
    completed_date = models.DateField(null=True, blank=True)

    def check_completion(self):
        """Check if all days in the program are completed by this user."""
        total_days = self.program.days.count()
        completed_days = self.user_profile.completed_days.filter(
            program=self.program
        ).count()

        if completed_days >= total_days and total_days > 0:
            self.status = "completed"
            self.completed_date = timezone.now().date()
            self.save(update_fields=["status", "completed_date"])
            return True
        return False

    class Meta:
        ordering = ["-assigned_date"]

    def __str__(self):
        return f"{self.user_profile.user.username} → {self.program.title}"
