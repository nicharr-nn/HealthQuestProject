from django.db import models
from django.contrib.auth.models import User
from coach.models import Coach


class Admin(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="admin_profile"
    )

    def __str__(self):
        return f"Moderator: {self.user.username}"
