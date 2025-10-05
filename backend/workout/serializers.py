from rest_framework import serializers

from .models import WorkoutDay, WorkoutProgram


class WorkoutDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutDay
        fields = ["id", "day_number", "title", "video_links", "duration"]


class WorkoutProgramSerializer(serializers.ModelSerializer):
    days = WorkoutDaySerializer(many=True, read_only=False)

    class Meta:
        model = WorkoutProgram
        fields = [
            "id",
            "coach",
            "title",
            "description",
            "level_access",
            "difficulty_level",
            "is_public",
            "duration",
            "category",
            "created_at",
            "updated_at",
            "days",
        ]

    def create(self, validated_data):
        days_data = validated_data.pop("days", [])
        program = WorkoutProgram.objects.create(**validated_data)
        for day_data in days_data:
            WorkoutDay.objects.create(program=program, **day_data)
        return program

    def update(self, instance, validated_data):
        days_data = validated_data.pop("days", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # overwrite days if sent
        if days_data:
            instance.days.all().delete()
            for day_data in days_data:
                WorkoutDay.objects.create(program=instance, **day_data)

        return instance
