from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer  # ← Add this import
from rest_framework import permissions, status
# from .serializers import RoleSelectionSerializer, OnboardingSerializer, UserProfileSerializer
from .serializers import UserProfileSerializer
from .models import User

# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def select_role(request):
#     """
#     API for role selection after OAuth registration
#     POST /api/auth/select-role/
#     Body: {"role": "user|coach|coachee"}
#     """
#     serializer = RoleSelectionSerializer(request.user, data=request.data, partial=True)
    
#     if serializer.is_valid():
#         user = serializer.save()
#         user.is_role_selected = True
#         user.save()
        
#         return Response({
#             'user': UserProfileSerializer(user).data,
#             'message': 'Role selected successfully'
#         }, status=status.HTTP_200_OK)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def complete_onboarding(request):
#     """
#     API to complete onboarding process
#     POST /api/auth/complete-onboarding/
#     Body: {"goal": "weight_loss", "age": 25, ...}
#     """
#     serializer = OnboardingSerializer(request.user, data=request.data, partial=True)
    
#     if serializer.is_valid():
#         user = serializer.save()
#         user.is_onboarding_complete = True
#         user.save()
        
#         return Response({
#             'user': UserProfileSerializer(user).data,
#             'message': 'Onboarding completed successfully'
#         }, status=status.HTTP_200_OK)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# @renderer_classes([JSONRenderer])
# @permission_classes([permissions.IsAuthenticated])
# def profile(request):
#     """
#     Get current user profile
#     GET /api/auth/profile/
#     """
#     serializer = UserProfileSerializer(request.user)
#     return Response(serializer.data)

# @api_view(['GET'])
# @renderer_classes([JSONRenderer])
# @permission_classes([permissions.AllowAny])
# def role_choices(request):
#     """
#     Get available role choices
#     GET /api/auth/role-choices/
#     """
#     try:
#         return Response({
#             'roles': [{'value': choice[0], 'label': choice[1]} for choice in User.USER_ROLES],
#             'goals': [{'value': choice[0], 'label': choice[1]} for choice in User.GOALS]
#         })
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
@permission_classes([permissions.AllowAny])
def current_user_view(request):
    """
    Retrieve current authenticated user profile
    """
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
@permission_classes([permissions.AllowAny])
def set_role_view(request):
    """
    Set/update user role
    """
    role = request.data.get("role")
    if role not in dict(User.ROLE_CHOICES):
        return Response(
            {"error": "Invalid role"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    user = request.user
    user.role = role
    user.save()
    
    return Response({
        "message": "Role updated successfully", 
        "role": role
    }, status=status.HTTP_200_OK)

@api_view(["POST"])
# @permission_classes([permissions.IsAuthenticated])
@permission_classes([permissions.AllowAny])
def set_about_you(request):
    data = request.data
    user = request.user

    user.height = data.get("height")
    user.weight = data.get("weight")
    user.age = data.get("age")
    user.save()

    return Response({"message": "About You saved successfully"})


@api_view(["PUT"])
# @permission_classes([IsAuthenticated])
@permission_classes([permissions.AllowAny])
def update_profile(request):
    user = request.user
    data = request.data

    # Example of updating fields (adapt to your model fields!)
    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    if hasattr(user, "height"):
        user.height = data.get("height", user.height)
    if hasattr(user, "weight"):
        user.weight = data.get("weight", user.weight)
    if hasattr(user, "goal"):
        user.goal = data.get("goal", user.goal)
    user.save()

    return Response({
        "message": "Profile updated successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "height": getattr(user, "height", None),
            "weight": getattr(user, "weight", None),
            "goal": getattr(user, "goal", None),
        }
    })

