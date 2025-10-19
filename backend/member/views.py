from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from member.models import CoachMemberRelationship
from member.serializers import CoachMemberRelationshipSerializer

@api_view(['GET', 'PATCH'])
def coach_member_requests(request, pk=None):
    user_profile = getattr(request.user, 'userprofile', None)
    coach_profile = getattr(user_profile, 'coach_profile', None)

    if not coach_profile:
        return Response({'error': 'You are not a coach'}, status=status.HTTP_403_FORBIDDEN)

    if pk:
        try:
            relationship = CoachMemberRelationship.objects.get(pk=pk, coach=coach_profile)
        except CoachMemberRelationship.DoesNotExist:
            return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'PATCH':
            new_status = request.data.get('status')
            if new_status:
                relationship.status = new_status
                relationship.save()
            serializer = CoachMemberRelationshipSerializer(relationship)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = CoachMemberRelationshipSerializer(relationship)
        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        relationships = CoachMemberRelationship.objects.filter(coach=coach_profile)
        serializer = CoachMemberRelationshipSerializer(relationships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def accepted_members(request):
    user_profile = getattr(request.user, 'userprofile', None)
    coach_profile = getattr(user_profile, 'coach_profile', None)

    if not coach_profile:
        return Response({'error': 'You are not a coach'}, status=status.HTTP_403_FORBIDDEN)

    relationships = CoachMemberRelationship.objects.filter(coach=coach_profile, status='approved')

    # convert to frontend format
    members_data = [
        {
            "memberId": r.member.member_id,
            "name": r.member.user.username,
            "email": r.member.user.email,
            "programName": r.member.program_name,
            "level": r.member.experience_level,
            "joinedAt": r.start_date,
            "lastActivity": r.member.lastActivity.strftime("%Y-%m-%d") if hasattr(r.member, 'lastActivity') else r.start_date
        }
        for r in relationships
    ]

    return Response(members_data, status=status.HTTP_200_OK)
