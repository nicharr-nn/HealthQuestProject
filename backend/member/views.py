from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from coach.models import Coach
from member.models import CoachMemberRelationship
from member.serializers import CoachMemberRelationshipSerializer


@api_view(['GET'])
def coach_member_requests(request):
    user_profile = getattr(request.user, 'userprofile', None)
    coach_profile = getattr(user_profile, 'coach_profile', None)

    if not coach_profile:
        return Response({'error': 'You are not a coach'}, status=status.HTTP_403_FORBIDDEN)

    relationships = CoachMemberRelationship.objects.filter(coach=coach_profile)

    serializer = CoachMemberRelationshipSerializer(relationships, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
