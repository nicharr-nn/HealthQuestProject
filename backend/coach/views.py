from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
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
            return Response({"error": "Coach profile not found"}, status=status.HTTP_404_NOT_FOUND)

        coach.bio = request.data.get("bio", coach.bio)
        if "certification_doc" in request.FILES:
            coach.certification_doc = request.FILES["certification_doc"]
        coach.status_approval = "pending"
        coach.approved_date = None
        coach.save()
        return Response(CoachSerializer(coach).data)

    elif request.method == "POST":
        coach = Coach.objects.create(
            user=profile,
            bio=request.data.get("bio", ""),
            certification_doc=request.FILES.get("certification_doc"),
            status_approval="pending",
            approved_date=None,
        )
        return Response(CoachSerializer(coach).data, status=status.HTTP_201_CREATED)



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
