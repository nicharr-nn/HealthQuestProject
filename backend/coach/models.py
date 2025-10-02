from django.db import models
from django.apps import apps
from users.models import UserProfile

class Coach(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    coach_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="coach_profile"
    )
    certification_doc = models.FileField(
        upload_to="coach_certifications/", null=True, blank=True
    )
    status_approval = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    bio = models.TextField(null=True, blank=True)
    approved_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Coach: {self.user.user.username} - Status: {self.status_approval}"
        
