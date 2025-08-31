from rest_framework import serializers
from .models import User

class RoleSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role']
    
    def validate_role(self, value):
        valid_roles = [choice[0] for choice in User.USER_ROLES]
        if value not in valid_roles:
            raise serializers.ValidationError("Invalid role selected")
        return value

class OnboardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['goal', 'age', 'height', 'weight']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 
                 'goal', 'age', 'height', 'weight', 
                 'is_role_selected', 'is_onboarding_complete']
        read_only_fields = ['id', 'username', 'email']