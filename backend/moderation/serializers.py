from rest_framework import serializers
from .models import Admin, AdminModeration


class AdminModerationSerializer(serializers.ModelSerializer):
    admin_name = serializers.CharField(
        source="admin.user.user.username", read_only=True
    )

    class Meta:
        model = AdminModeration
        fields = "__all__"


class AdminSerializer(serializers.ModelSerializer):
    admin_name = serializers.CharField(
        source="admin.user.user.username", read_only=True
    )

    class Meta:
        model = Admin
        fields = "__all__"
