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

                # When coach accepts, also activate the member
                member = relationship.member
                if new_status in ['accepted', 'approved']:
                    # Update member status to approve
                    if hasattr(member, 'status'):
                        member.status = 'approved'
                    member.save()

                elif new_status == 'rejected':
                    # Optionally reset member to pending or inactive
                    if hasattr(member, 'status'):
                        member.status = 'pending'
                        member.save()


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
        status__in=['accepted', 'approved']
    )

    # convert to frontend format
    members_data = [
        {
            "memberId": r.member.member_id,
            "name": r.member.user.user.username,
            "programName": r.member.program_name,
            "joinedAt": r.member.submitted_at,
            "experienceLevel": r.member.experience_level,
        }
        for r in relationships
    ]

    return Response(members_data, status=status.HTTP_200_OK)

@api_view(["POST", "PATCH"])
@permission_classes([IsAuthenticated])
def apply_as_member(request):
    """
    Create or update a Member profile for the authenticated user.
    Members can use public_id (like C_A1B2C3D4) to request coaches.
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
            "experience_level": request.data.get("experience_level", "beginner"),
            "program_name": None,
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
            # Try to find coach by public_id first
            if coach_code.startswith('C-'):
                coach = Coach.objects.get(public_id=coach_code)
            else:
                # Fallback: try primary key or username
                try:
                    # Try as primary key
                    coach = Coach.objects.get(pk=int(coach_code))
                except (ValueError, Coach.DoesNotExist):
                    # Try as username
                    coach = Coach.objects.get(user__user__username=coach_code)
            
            # Check if relationship already exists
            existing_relationship = CoachMemberRelationship.objects.filter(
                member=member
            ).first()
            
            if existing_relationship:
                current_coach_name = existing_relationship.coach.user.user.username
                return Response(
                    {
                        "error": f"You already have a {existing_relationship.status} relationship with coach {current_coach_name}. Please cancel it first to request a new coach."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            # Create new relationship
            relationship = CoachMemberRelationship.objects.create(
                coach=coach, 
                member=member, 
                status="pending"
            )
            
            # Return success response with coach info
            return Response(
                {
                    "message": f"Request sent successfully to coach {coach.user.user.username}!",
                    "member": MemberSerializer(member).data,
                    "coach": {
                        "name": coach.user.user.username,
                        "public_id": coach.public_id,
                    },
                    "status": "pending"
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            )
            
        except Coach.DoesNotExist:
            # Provide helpful error message with available coaches
            available_coaches = Coach.objects.filter(status_approval='approved')[:5]
            coach_list = [
                {
                    'public_id': coach.public_id,
                    'name': coach.user.user.username,
                }
                for coach in available_coaches
            ]
            
            return Response(
                {
                    "error": f"Coach with code '{coach_code}' not found.",
                    "available_coaches": coach_list,
                    "hint": "Try one of these available coach codes"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to create relationship: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
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

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def assign_program_to_member(request, member_id):
    """
    Coach assigns a workout program to an accepted member.
    """
    user_profile = getattr(request.user, "userprofile", None)
    coach_profile = getattr(user_profile, "coach_profile", None)

    if not coach_profile:
        return Response({"error": "You are not a coach."}, status=403)

    try:
        relationship = CoachMemberRelationship.objects.get(
            coach=coach_profile, member__member_id=member_id, status="accepted"
        )
    except CoachMemberRelationship.DoesNotExist:
        return Response({"error": "No such accepted member."}, status=404)

    program_name = request.data.get("program_name")
    if not program_name:
        return Response({"error": "Program name required."}, status=400)

    relationship.member.program_name = program_name
    relationship.member.save()

    return Response(
        {"message": f"Program '{program_name}' assigned to member."},
        status=200,
    )