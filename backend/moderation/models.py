from django.db import models
from django.contrib.auth.models import User
from coach.models import Coach


class Admin(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="admin_profile"
    )

    def __str__(self):
        return f"Moderator: {self.user.username}"


class AdminModeration(models.Model):
    CONTENT_TYPE_CHOICES = [
        ("post", "Post"),
        ("user", "User"),
        ("coach_certification", "Coach Certification"),
    ]

    ACTION_CHOICES = [
        ("delete_post", "Delete Post"),
        ("delete_user", "Delete User Account"),
        ("delete_recipe", "Delete Recipe"),
        ("approve_certification", "Approve Coach Certification"),
        ("reject_certification", "Reject Coach Certification"),
    ]

    admin = models.ForeignKey(
        Admin, on_delete=models.CASCADE, related_name="moderations"
    )
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.CharField(max_length=30, choices=CONTENT_TYPE_CHOICES)
    content_id = models.PositiveIntegerField(null=True, blank=True)
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    reason = models.TextField()
    moderated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.admin.user.username} "
            f"{self.get_action_display()} "
            f"(ID {self.content_id})"
        )