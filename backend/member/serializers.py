from rest_framework import serializers
from member.models import CoachMemberRelationship


class CoachMemberRelationshipSerializer(serializers.ModelSerializer):
    memberName = serializers.CharField(source='member.user.username')
    memberId = serializers.CharField(source='member.member_id')
    email = serializers.CharField(source='member.user.email')
    programName = serializers.CharField(source='member.program_name', default='')
    experienceLevel = serializers.CharField(source='member.experience_level')
    goals = serializers.ListField(source='member.goals', required=False)
    message = serializers.CharField(source='member.message', required=False)
    status = serializers.CharField()

    class Meta:
        model = CoachMemberRelationship
        fields = [
            'relationship_id', 'memberName', 'memberId',
            'email', 'programName', 'experienceLevel',
            'goals', 'message', 'status', 'start_date'
        ]
