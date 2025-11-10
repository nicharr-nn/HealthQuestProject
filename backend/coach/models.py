from django.db import models

from users.models import UserProfile


class Coach(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    coach_id = models.AutoField(primary_key=True)
    public_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
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
        # Check if status is being changed to "approved" and public_id doesn't exist
        if self.status_approval == "approved" and not self.public_id:
            # First save to get coach_id if this is a new object
            if not self.coach_id:
                super().save(*args, **kwargs)
            
            # Generate public_id
            self.public_id = f"C-{self.coach_id:05d}"
            
            # Set approved_date if not set
            if not self.approved_date:
                from django.utils import timezone
                self.approved_date = timezone.now()
        
        super().save(*args, **kwargs)

    def __str__(self):
        public_id_display = self.public_id if self.public_id else "No ID"
        return (
            f"Coach: {self.user.user.username} ({public_id_display}) "
            f"- Status: {self.status_approval}"
        )
    