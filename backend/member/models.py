from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Member(models.Model):
    EXPERIENCE_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    member_id = models.CharField(max_length=20, unique=True)
    experience_level = models.CharField(
        max_length=12,
        choices=EXPERIENCE_LEVEL_CHOICES,
        default='beginner'
    )
    program_name = models.CharField(max_length=255, blank=True, null=True)
    goals = models.JSONField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending',
    )

    def __str__(self):
        return f"{self.user.username} ({self.member_id})"


class CoachMemberRelationship(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    relationship_id = models.AutoField(primary_key=True)
    coach = models.ForeignKey(
        'coach.Coach', on_delete=models.CASCADE, related_name='relationships'
    )
    member = models.OneToOneField(
        'Member', on_delete=models.CASCADE, related_name='relationship'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.coach} → {self.member} ({self.status})"
