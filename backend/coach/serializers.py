from rest_framework import serializers

from .models import Coach


class CoachSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    certification_doc = serializers.FileField(required=False, allow_null=True)

    def get_name(self, obj):
        # Defensive: handles both Django User full_name and fallback to username
        user = getattr(obj.user, "user", None)
        if user:
            return user.get_full_name() or user.username
        return "Unknown"

    class Meta:
        model = Coach
        fields = [
            'user',
            "coach_id",
            "public_id",
            "name",
            "certification_doc",
            "status_approval",
            "bio",
            "approved_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "status_approval",
            "approved_date",
            "certification_doc",
        ]
