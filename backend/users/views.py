from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
from .serializers import UserProfileSerializer, UserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """Get user information + profile status"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    serializer = UserSerializer(request.user)
    data = serializer.data

    # Add "profile_complete" flag
    data["profile_complete"] = all([
        profile.role,
        profile.height,
        profile.weight,
        profile.age,
        profile.gender,
        profile.location
    ])

    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @csrf_exempt
def set_role(request):
    """Set user role"""
    try:
        profile = request.user.userprofile
        profile.role = request.data.get('role')
        profile.save()
        return Response({'status': 'success', 'role': profile.role})
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @csrf_exempt
def update_profile(request):
    """Update user profile data"""
    try:
        profile = request.user.userprofile
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data})
        return Response({'status': 'error', 'errors': serializer.errors}, status=400)
        
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=400)