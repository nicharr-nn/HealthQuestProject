from django.db import models

from users.models import UserProfile


class Coach(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    coach_id = models.AutoField(primary_key=True)
    public_id = models.CharField(max_length=20, unique=True, blank=True)
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="coach_profile"
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

    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = f"C-{self.coach_id or 0:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return (f"Coach: {self.user.user.username} ({self.public_id}) "
                f"- Status: {self.status_approval}")
