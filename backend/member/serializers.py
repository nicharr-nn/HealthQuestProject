from rest_framework import serializers
from member.models import CoachMemberRelationship, Member
from users.models import FitnessGoal
from users.serializers import FitnessGoalSerializer
from coach.serializers import CoachSerializer

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            'member_id', 'user', 'experience_level', 'program_name',
            'message', 'submitted_at', 'status'
        ]

class CoachMemberRelationshipSerializer(serializers.ModelSerializer):
    coach = CoachSerializer(read_only=True)
    memberName = serializers.CharField(source='member.user.user.username', read_only=True)
    memberId = serializers.CharField(source='member.member_id', read_only=True)
    experienceLevel = serializers.CharField(source='member.experience_level', read_only=True)
    message = serializers.CharField(source='member.message', read_only=True)
    programName = serializers.CharField(source='member.program_name', read_only=True)
    submittedAt = serializers.DateTimeField(source='member.submitted_at', read_only=True)
    goals = serializers.SerializerMethodField()

    def get_goals(self, obj):
        fitness_goals = FitnessGoal.objects.filter(user_profile=obj.member.user)
        return [goal.get_goal_type_display() for goal in fitness_goals]

    class Meta:
        model = CoachMemberRelationship
        fields = [
            'relationship_id',
            'coach',
            'status',
            'memberName',
            'memberId',
            'experienceLevel',
            'message',
            'programName',
            'submittedAt',
            'goals',
        ]


# class FoodPostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FoodPost
#         fields = ["id", "title", "content", "image", "created_at", "updated_at"]
#         read_only_fields = ["id", "created_at", "updated_at"]

#     def create(self, validated_data):
#         user = self.context["request"].user
#         user_profile = user.userprofile

#         if user_profile.role != "member":
#             raise serializers.ValidationError("Only members can create food posts.")

#         # Find active coach relationship
#         rel = CoachMemberRelationship.objects.filter(
#             member=user_profile, status="accepted"
#         ).first()

#         if not rel:
#             raise serializers.ValidationError(
#                 "You don't have an active coach assigned."
#             )

#         validated_data["user_profile"] = user_profile
#         validated_data["coach"] = rel.coach

#         return super().create(validated_data)
