from rest_framework import status
from rest_framework.decorators import (
    api_view,
    parser_classes,
    permission_classes,
)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Coach
from .serializers import CoachSerializer


@api_view(["POST", "PATCH"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_certification(request):
    profile = request.user.userprofile

    if request.method == "PATCH":
        try:
            coach = Coach.objects.get(user=profile)
        except Coach.DoesNotExist:
            return Response(
                {"error": "Coach profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        coach.bio = request.data.get("bio", coach.bio)
        if "certification_doc" in request.FILES:
            coach.certification_doc = request.FILES["certification_doc"]
        coach.status_approval = "pending"
        coach.approved_date = None
        coach.save()
        return Response(CoachSerializer(coach).data)

    elif request.method == "POST":
        # Avoid IntegrityError when a Coach record already exists for this user.
        # If a coach exists, update it; otherwise create a new one.
        coach, created = Coach.objects.get_or_create(
            user=profile,
            defaults={
                "bio": request.data.get("bio", ""),
                "certification_doc": request.FILES.get("certification_doc"),
                "status_approval": "pending",
                "approved_date": None,
            },
        )
        if not created:
            # update existing coach entry (treat POST as upsert for UX)
            coach.bio = request.data.get("bio", coach.bio)
            if "certification_doc" in request.FILES:
                coach.certification_doc = request.FILES["certification_doc"]
            coach.status_approval = "pending"
            coach.approved_date = None
            coach.save()
            return Response(
                CoachSerializer(coach).data, status=status.HTTP_200_OK
            )

        return Response(
            CoachSerializer(coach).data, status=status.HTTP_201_CREATED
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def coach_status(request):
    """
    Return the current coach profile and status for the logged-in user.
    """
    user_profile = getattr(request.user, "userprofile", None)
    if not user_profile:
        return Response({"coach": None})

    try:
        coach = user_profile.coach_profile
        serializer = CoachSerializer(coach)
        return Response({"coach": serializer.data})
    except Coach.DoesNotExist:
        return Response({"coach": None})


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def edit_coach_profile(request):
    """Edit coach profile (bio, name, etc.)"""
    try:
        profile = request.user.userprofile
        coach = profile.coach_profile  # reverse relation

        # Update only allowed fields
        if "bio" in request.data:
            coach.bio = request.data["bio"]

        if "name" in request.data:
            # Assuming your Coach model has a name field
            coach.name = request.data["name"]

        coach.save()
        return Response(CoachSerializer(coach).data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
