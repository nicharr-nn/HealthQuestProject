from rest_framework import serializers
from django.contrib.auth.models import User
from django.apps import apps
from .models import Coach


def get_user_profile_model():
    return apps.get_model("users", "UserProfile")


def get_fitness_goal_model():
    return apps.get_model("users", "FitnessGoal")


class FitnessGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_fitness_goal_model()
        fields = ["id", "goal_type", "start_date", "end_date"]
        read_only_fields = ["id", "start_date"]


class UserProfileSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(use_url=True, required=False, allow_null=True)
    fitness_goals = FitnessGoalSerializer(many=True, read_only=True)
    current_goal = serializers.SerializerMethodField()

    class Meta:
        model = get_user_profile_model()
        fields = [
            "role",
            "height",
            "weight",
            "age",
            "gender",
            "location",
            "photo",
            "fitness_goals",
            "current_goal",
        ]
        read_only_fields = ["role"]

    def get_current_goal(self, obj):
        """Return the most recent fitness goal type for normal users."""
        if obj.role == "normal":
            latest_goal = obj.fitness_goals.order_by("-start_date").first()
            if latest_goal:
                return latest_goal.goal_type
        return None


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source="userprofile")
    is_admin = serializers.SerializerMethodField()
    profile_complete = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profile",
            "is_admin",
            "profile_complete",
        ]

    def get_is_admin(self, obj):
        return obj.is_superuser or (
            hasattr(obj, "userprofile") and obj.userprofile.role == "admin"
        )

    def get_profile_complete(self, obj):
        """Check if the user profile has all required fields filled."""
        if hasattr(obj, "userprofile"):
            profile = obj.userprofile
            return all(
                [
                    profile.height is not None,
                    profile.weight is not None,
                    profile.age is not None,
                    profile.gender is not None,
                    profile.location is not None,
                ]
            )
        return False

    def update(self, instance, validated_data):
        """Handle nested profile updates safely."""
        UserProfile = get_user_profile_model()
        profile_data = validated_data.pop("userprofile", {})

        # Update User fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create UserProfile
        profile, created = UserProfile.objects.get_or_create(user=instance)
        for attr, value in profile_data.items():
            if attr != "role":  # Prevent role change through this serializer
                setattr(profile, attr, value)
        profile.save()

        return instance


class CoachSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # shows username
    certification_doc = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Coach
        fields = [
            "coach_id",
            "user",
            "certification_doc",
            "status_approval",
            "bio",
            "approved_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["coach_id", "status_approval", "approved_date", "created_at", "updated_at"]