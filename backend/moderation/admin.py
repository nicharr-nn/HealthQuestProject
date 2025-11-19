from django.contrib import admin
from .models import Admin, AdminModeration


@admin.register(Admin)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]
    search_fields = ["user__username"]


@admin.register(AdminModeration)
class AdminModerationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "admin",
        "content_type",
        "content_id",
        "action",
        "reason",
        "moderated_at",
    ]
    list_filter = ["action", "content_type", "moderated_at"]
    search_fields = ["admin__user__username", "reason"]
