from rest_framework import serializers
from .models import FoodPost, CoachMemberRelationship


class FoodPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodPost
        fields = ["id", "title", "content", "image", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        user_profile = user.userprofile

        if user_profile.role != "member":
            raise serializers.ValidationError("Only members can create food posts.")

        # Find active coach relationship
        rel = CoachMemberRelationship.objects.filter(
            member=user_profile, status="accepted"
        ).first()

        if not rel:
            raise serializers.ValidationError(
                "You don't have an active coach assigned."
            )

        validated_data["user_profile"] = user_profile
        validated_data["coach"] = rel.coach

        return super().create(validated_data)
