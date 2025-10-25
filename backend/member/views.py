from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Member, CoachMemberRelationship
from .serializers import CoachMemberRelationshipSerializer, MemberSerializer
from coach.models import Coach


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def coach_member_requests(request, pk=None):
    user_profile = getattr(request.user, 'userprofile', None)
    coach_profile = getattr(user_profile, 'coach_profile', None)

    if not coach_profile:
        return Response(
            {'error': 'You are not a coach'},
            status=status.HTTP_403_FORBIDDEN
        )

    if pk:
        try:
            relationship = CoachMemberRelationship.objects.get(
                pk=pk, coach=coach_profile
            )
        except CoachMemberRelationship.DoesNotExist:
            return Response(
                {'error': 'Request not found'},
                status=status.HTTP_404_NOT_FOUND
            )

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
@permission_classes([IsAuthenticated])
def accepted_members(request):
    user_profile = getattr(request.user, 'userprofile', None)
    coach_profile = getattr(user_profile, 'coach_profile', None)

    if not coach_profile:
        return Response(
            {'error': 'You are not a coach'},
            status=status.HTTP_403_FORBIDDEN
        )

    relationships = CoachMemberRelationship.objects.filter(
        coach=coach_profile,
        status='approved'
    )

    # convert to frontend format
    members_data = [
        {
            "memberId": r.member.member_id,
            "name": r.member.user.username,
            "programName": r.member.program_name,
            "joinedAt": r.start_date,
            "lastActivity": (
                r.member.lastActivity.strftime("%Y-%m-%d")
                if hasattr(r.member, "lastActivity")
                else r.start_date
            ),
        }
        for r in relationships
    ]

    return Response(members_data, status=status.HTTP_200_OK)

@api_view(["POST", "PATCH"])
@permission_classes([IsAuthenticated])
def apply_as_member(request):
    """
    Create or update a Member profile for the authenticated user.
    Ensures user.role = 'member' and assigns the selected coach if provided.
    """
    profile = request.user.userprofile

    # Ensure role is 'member'
    if profile.role != "member":
        profile.role = "member"
        profile.save()

    # Create or update member profile
    member, created = Member.objects.get_or_create(
        user=profile,
        defaults={
            "member_id": f"M-{profile.user.id:05d}",
            "experience_level": request.data.get("experience_level", "beginner"),
            "program_name": None,  # Coach will assign later
            "message": request.data.get("message", ""),
        },
    )

    # Update fields if PATCH or if already exists
    if not created or request.method == "PATCH":
        member.experience_level = request.data.get(
            "experience_level", member.experience_level
        )
        member.message = request.data.get("message", member.message)
        member.save()
    
    coach_code = request.data.get("coach_code")
    if coach_code:
        try:
            coach = Coach.objects.get(public_id=coach_code)
            CoachMemberRelationship.objects.get_or_create(
                coach=coach, member=member, defaults={"status": "pending"}
            )
        except Coach.DoesNotExist:
            return Response(
                {"error": "Invalid coach code."},
                status=status.HTTP_404_NOT_FOUND,
            )


        return Response(
        MemberSerializer(member).data,
        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
    )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_member_profile(request):
    """
    Retrieve the Member profile for the authenticated user.
    """
    profile = request.user.userprofile

    try:
        member = Member.objects.get(user=profile)
        serializer = MemberSerializer(member)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Member.DoesNotExist:
        return Response(
            {"error": "Member profile not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
    
@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def manage_member_request(request):
    """
    Member can:
      - GET: view their coach request(s)
      - PATCH: update their message or experience_level
      - DELETE: cancel the request
    """
    profile = request.user.userprofile

    try:
        member = Member.objects.get(user=profile)
    except Member.DoesNotExist:
        return Response({"error": "You are not a member."}, status=status.HTTP_404_NOT_FOUND)

    try:
        relationship = CoachMemberRelationship.objects.get(member=member)
    except CoachMemberRelationship.DoesNotExist:
        return Response({"message": "No coach request found."}, status=status.HTTP_200_OK)

    if request.method == "GET":
        serializer = CoachMemberRelationshipSerializer(relationship)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PATCH":
        new_message = request.data.get("message")
        new_level = request.data.get("experience_level")

        if new_message:
            member.message = new_message
        if new_level:
            member.experience_level = new_level
        member.save()

        serializer = MemberSerializer(member)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # DELETE (cancel request)
    elif request.method == "DELETE":
        relationship.delete()
        return Response(
            {"message": "Your coach request has been cancelled."},
            status=status.HTTP_204_NO_CONTENT,
        )

# @api_view(["PATCH"])
# @permission_classes([IsAuthenticated])
# def assign_program_to_member(request, member_id):
#     """
#     Coach assigns a workout program to an accepted member.
#     """
#     user_profile = getattr(request.user, "userprofile", None)
#     coach_profile = getattr(user_profile, "coach_profile", None)

#     if not coach_profile:
#         return Response({"error": "You are not a coach."}, status=403)

#     try:
#         relationship = CoachMemberRelationship.objects.get(
#             coach=coach_profile, member__member_id=member_id, status="accepted"
#         )
#     except CoachMemberRelationship.DoesNotExist:
#         return Response({"error": "No such accepted member."}, status=404)

#     program_name = request.data.get("program_name")
#     if not program_name:
#         return Response({"error": "Program name required."}, status=400)

#     relationship.member.program_name = program_name
#     relationship.member.save()

#     return Response(
#         {"message": f"Program '{program_name}' assigned to member."},
#         status=200,
#     )
