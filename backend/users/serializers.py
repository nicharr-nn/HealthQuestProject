from rest_framework import serializers
from .models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 
        #          'goal', 'age', 'height', 'weight', 
        #          'is_role_selected', 'is_onboarding_complete']
        # read_only_fields = ['id', 'username', 'email']
        fields = ["id", "email", "role", "height", "weight", "age"]