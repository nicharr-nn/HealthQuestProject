from rest_framework import serializers
from .models import Recipe, RecipeRating

from users.models import UserProfile


# class UserProfileSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source="user.username", read_only=True)

#     class Meta:
#         model = UserProfile
#         fields = ["id", "username"]


class RecipeSerializer(serializers.ModelSerializer):
    user_profile = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField(source="user_profile.user.id", read_only=True)
    user_profile_username = serializers.CharField(
        source="user_profile.username", read_only=True
    )
    image = serializers.ImageField(use_url=True, required=False, allow_null=True)
    pdf_file = serializers.FileField(use_url=True, required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "user_profile",
            "user_id",
            "user_profile_username",
            "title",
            "ingredients",
            "steps",
            "access_level",
            "image",
            "pdf_file",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user_profile", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context["request"]
        user_profile = request.user.userprofile

        # Fetch current level safely
        current_level = user_profile.get_current_level().level.lower()
        role = user_profile.role.lower()

        # Access control: only coaches or gold users can create
        if not (role == "coach" or current_level == "gold"):
            raise serializers.ValidationError(
                "Only coaches and Gold-level users can create recipes."
            )

        validated_data["user_profile"] = user_profile
        return super().create(validated_data)

    def get_user_profile(self, obj):
        # Keep returning the username for backward compatibility
        return f"{obj.user_profile.first_name}- {obj.user_profile.role}"


class RecipeRatingSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user_profile.user.username", read_only=True)

    class Meta:
        model = RecipeRating
        fields = ["id", "user", "rating", "created_at"]
