from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer  # ← Add this import
from .serializers import RoleSelectionSerializer, OnboardingSerializer, UserProfileSerializer
from .models import User

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def select_role(request):
    """
    API for role selection after OAuth registration
    POST /api/auth/select-role/
    Body: {"role": "user|coach|coachee"}
    """
    serializer = RoleSelectionSerializer(request.user, data=request.data, partial=True)
    
    if serializer.is_valid():
        user = serializer.save()
        user.is_role_selected = True
        user.save()
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'message': 'Role selected successfully'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def complete_onboarding(request):
    """
    API to complete onboarding process
    POST /api/auth/complete-onboarding/
    Body: {"goal": "weight_loss", "age": 25, ...}
    """
    serializer = OnboardingSerializer(request.user, data=request.data, partial=True)
    
    if serializer.is_valid():
        user = serializer.save()
        user.is_onboarding_complete = True
        user.save()
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'message': 'Onboarding completed successfully'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    """
    Get current user profile
    GET /api/auth/profile/
    """
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([permissions.AllowAny])
def role_choices(request):
    """
    Get available role choices
    GET /api/auth/role-choices/
    """
    try:
        return Response({
            'roles': [{'value': choice[0], 'label': choice[1]} for choice in User.USER_ROLES],
            'goals': [{'value': choice[0], 'label': choice[1]} for choice in User.GOALS]
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

