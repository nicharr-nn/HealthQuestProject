from django.db import models
from users.models import UserProfile


class FoodPost(models.Model):
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='food_posts'
    )
    coach = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='coach_food_posts'
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='food_posts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.title or 'Food Post'}"

    class Meta:
        ordering = ['-created_at']

