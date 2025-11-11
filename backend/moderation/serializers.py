from rest_framework import serializers
from .models import AdminModeration


class AdminModerationSerializer(serializers.ModelSerializer):
    admin_name = serializers.CharField(
        source="admin.user.user.username", read_only=True
    )

    class Meta:
        model = AdminModeration
        fields = "__all__"
