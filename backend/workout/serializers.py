from rest_framework import serializers

from .models import WorkoutDay, WorkoutProgram
from .models import WorkoutAssignment


class WorkoutDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutDay
        fields = ["id", "day_number", "title", "video_links", "duration"]


class WorkoutProgramSerializer(serializers.ModelSerializer):
    days = WorkoutDaySerializer(many=True, read_only=False)
    assigned_member_id = serializers.SerializerMethodField()  # if assigned to a member

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
            "assigned_member_id",
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

    def get_assigned_member_id(self, obj):
        assignment = WorkoutAssignment.objects.filter(program=obj).first()
        return assignment.member.member_id if assignment else None


class WorkoutAssignmentSerializer(serializers.ModelSerializer):
    program = WorkoutProgramSerializer(read_only=True)
    member_name = serializers.CharField(
        source="member.user.user.username", read_only=True
    )
    member_id = serializers.CharField(source="member.member_id", read_only=True)
    coach_name = serializers.CharField(
        source="program.coach.user.username", read_only=True
    )

    class Meta:
        model = WorkoutAssignment
        fields = [
            "id",
            "member_name",
            "member_id",
            "coach_name",
            "program",
            "status",
            "assigned_date",
            "due_date",
            "completed_date",
        ]
        read_only_fields = fields
