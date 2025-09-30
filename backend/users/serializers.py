from rest_framework import serializers
from django.contrib.auth.models import User
from django.apps import apps
from fitness.serializers import FitnessGoalSerializer


def get_user_profile_model():
    return apps.get_model("users", "UserProfile")


def get_user_level_model():
    return apps.get_model("users", "UserLevel")


def get_workout_completion_model():
    return apps.get_model("users", "WorkoutCompletion")


def get_workout_assignment_model():
    return apps.get_model("users", "WorkoutAssignment")

def get_workout_program_model():
    return apps.get_model("users", "WorkoutProgram")

class WorkoutProgramSerializer(serializers.ModelSerializer):
    coach_name = serializers.CharField(source="coach.user.username", read_only=True)

    class Meta:
        model = get_workout_program_model()
        fields = [
            "id",
            "coach",
            "coach_name",
            "title",
            "description",
            "video_links",
            "level_access",
            "difficulty_level",
            "is_public",
            "duration",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "coach_name", "created_at", "updated_at"]


class UserLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_level_model()
        fields = ["level_rank", "level", "xp", "goal_achieved"]

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
