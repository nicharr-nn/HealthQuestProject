from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FitnessGoal, User

@api_view(['POST'])
def select_goal(request):
    user_id = request.data.get('user_id')
    role = request.data.get('role')  # expecting 'role'
    
    try:
        user = User.objects.get(user_id=user_id)
        user.role = role
        user.save()
        return Response({'success': True, 'role': role})
    except User.DoesNotExist:
        return Response({'success': False, 'error': 'User not found'}, status=404)
