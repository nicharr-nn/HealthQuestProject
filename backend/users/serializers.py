# users/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['role', 'height', 'weight', 'age', 'gender', 'location']
        read_only_fields = ['role']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='userprofile')
    is_admin = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile', 'is_admin']
    
    def get_is_admin(self, obj):
        return obj.is_superuser or (hasattr(obj, 'userprofile') and obj.userprofile.role == 'admin')