from django.contrib import admin

from .models import UserProfile, UserLevel


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "age", "gender", "location", "created_at"]
    list_filter = ["role", "gender", "location"]
    search_fields = ["user__username", "user__email", "location"]
    ordering = ["-created_at"]


admin.site.register(UserLevel)
