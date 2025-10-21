from rest_framework import serializers
from .models import WorkoutAssignment

class WorkoutAssignmentSerializer(serializers.ModelSerializer):
    program_title = serializers.CharField(source="program.title", read_only=True)
    member_name = serializers.CharField(source="user.username", read_only=True)
    member_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = WorkoutAssignment
        fields = [
            "id",
            "member_name",
            "member_id",
            "program_title",
            "status",
            "assigned_date",
            "due_date",
            "completed_date",
        ]
        read_only_fields = fields
        ordering = ["-assigned_date"]