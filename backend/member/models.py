from django.db import models
from users.models import UserProfile


class Member(models.Model):
    EXPERIENCE_LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="member_profile"
    )
    member_id = models.CharField(max_length=20, unique=True)
    experience_level = models.CharField(
        max_length=12, choices=EXPERIENCE_LEVEL_CHOICES, default="beginner"
    )
    program_name = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="pending",
    )

    def __str__(self):
        return f"{self.user.user.username} ({self.member_id} - {self.status})"


class CoachMemberRelationship(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    relationship_id = models.AutoField(primary_key=True)
    coach = models.ForeignKey(
        "coach.Coach", on_delete=models.CASCADE, related_name="relationships"
    )
    member = models.OneToOneField(
        "Member", on_delete=models.CASCADE, related_name="relationship"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.coach} → {self.member} ({self.status})"


class FoodPost(models.Model):
    """Members post their meals for their coach to review"""

    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="food_posts"
    )
    coach = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="coach_food_posts"
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to="food_posts/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.title or 'Food Post'}"

    class Meta:
        ordering = ["-created_at"]


class FoodPostComment(models.Model):
    """Coaches can comment on member food posts to provide feedback"""

    food_post = models.ForeignKey(
        FoodPost, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="food_post_comments"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.user.username} on {self.food_post}"

    class Meta:
        ordering = ["created_at"]
