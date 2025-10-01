from rest_framework import serializers
from django.apps import apps

def get_workout_completion_model():
    return apps.get_model("workout", "WorkoutDayCompletion")

def get_workout_assignment_model():
    return apps.get_model("workout", "WorkoutAssignment")

def get_workout_program_model():
    return apps.get_model("workout", "WorkoutProgram")

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

class WorkoutDayCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_workout_completion_model()
        fields = ["id", "assignment", "xp_earned", "completed_at"]
