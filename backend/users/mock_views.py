from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions

@api_view(["GET"])
@permission_classes([permissions.AllowAny])  # no login required
def dev_mock_user(request):
    """
    Return mock user profile for frontend demo
    """
    data = {
        "id": 1,
        "name": "Jane Doe",
        "email": "jane@example.com",
        "height": 165,
        "weight": 55,
        "goal": "Stay Healthy",
        "location": "Thailand",
        "joinDate": "2025-09-04",
    }
    return Response(data)
