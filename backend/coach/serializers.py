from rest_framework import serializers
from django.apps import apps
from .models import Coach

class CoachSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    certification_doc = serializers.FileField(required=False, allow_null=True)

    def get_name(self, obj):
        return obj.user.user.get_full_name()  # Google name

    class Meta:
        model = Coach
        fields = [
            "coach_id",
            "name",
            "certification_doc",
            "status_approval",
            "bio",
            "approved_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["coach_id", "name", "status_approval", "approved_date", "created_at", "updated_at"]