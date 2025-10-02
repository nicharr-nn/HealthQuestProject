from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.core.files.storage import default_storage
from .models import Coach, UserProfile
from .serializers import CoachSerializer
from django.utils.timezone import now

@api_view(['POST', 'PATCH'])
@permission_classes([IsAuthenticated])
def upload_certification(request):
    user_profile = request.user.userprofile

    try:
        coach = Coach.objects.get(user=user_profile)
        serializer = CoachSerializer(coach, data=request.data, partial=True)
    except Coach.DoesNotExist:
        serializer = CoachSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

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
