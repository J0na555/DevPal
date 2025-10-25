from rest_framework import serializers
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'created_at', 'skills', 'interests', 'availability_hours', 'preferred_roles']
        read_only_fields = ['id', 'created_at']
