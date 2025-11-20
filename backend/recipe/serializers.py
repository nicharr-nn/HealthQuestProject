from rest_framework import serializers
from .models import Recipe, RecipeRating


class RecipeSerializer(serializers.ModelSerializer):
    user_profile = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    user_profile_username = serializers.SerializerMethodField()
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
        read_only_fields = [
            "id",
            "user_profile",
            "user_id",
            "user_profile_username",
            "created_at",
            "updated_at",
        ]

    def get_user_profile(self, obj):
        """Return a display name for the recipe owner ("First Last" or username)."""
        user = obj.user_profile.user
        full_name = f"{user.first_name} {user.last_name}".strip()
        return full_name if full_name else user.username

    def get_user_id(self, obj):
        try:
            return obj.user_profile.user.id
        except AttributeError:
            return None

    def get_user_profile_username(self, obj):
        try:
            return obj.user_profile.user.username
        except AttributeError:
            return None

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


class RecipeRatingSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user_profile.user.username", read_only=True)

    class Meta:
        model = RecipeRating
        fields = ["id", "user", "rating", "created_at"]
