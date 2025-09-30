from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.apps import apps
from .models import FitnessGoal
from users.serializers import UserSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_goal(request):
    """Set user fitness goal"""
    from django.apps import apps

    FitnessGoal = apps.get_model("fitness", "FitnessGoal")

    try:
        profile = request.user.userprofile

        # Only normal users can have fitness goals
        if profile.role != "normal":
            return Response(
                {"detail": "Only normal users can set fitness goals."}, status=400
            )

        goal_type = request.data.get("goal_type")
        end_date = request.data.get("end_date")

        if not goal_type:
            return Response({"detail": "Goal type is required."}, status=400)

        # Create new FitnessGoal
        FitnessGoal.objects.create(
            user_profile=profile, goal_type=goal_type, end_date=end_date
        )

        # Serialize the updated user profile

        serializer = UserSerializer(request.user)

        return Response({"status": "success", "user": serializer.data})

    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=400)
