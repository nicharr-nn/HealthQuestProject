from django.contrib import admin
from .models import Admin, AdminModeration


@admin.register(Admin)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    search_fields = ['user__username']


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
    list_display = ['admin', 'coach', 'content_type', 'content_id', 'action', 'reason', 'moderated_at']
    search_fields = ['user__username']

    # admin = models.ForeignKey(
    #     Admin, on_delete=models.CASCADE, related_name="moderations"
    # )
    # coach = models.ForeignKey(Coach, on_delete=models.CASCADE, null=True, blank=True)
    # content_type = models.CharField(max_length=30, choices=CONTENT_TYPE_CHOICES)
    # content_id = models.PositiveIntegerField(null=True, blank=True)
    # action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    # reason = models.TextField()
    # moderated_at = models.DateTimeField(auto_now_add=True)