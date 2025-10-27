from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UserProfile

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'bio', 'created_at', 'skills', 'interests', 'availability_hours', 'preferred_roles']
        read_only_fields = ['id', 'created_at']


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, min_length=6)
    bio = serializers.CharField(required=False, allow_blank=True)
    skills = serializers.ListField(child=serializers.CharField(), required=False)
    interests = serializers.ListField(child=serializers.CharField(), required=False)
    availability_hours = serializers.IntegerField(required=False, default=10)
    preferred_roles = serializers.ListField(child=serializers.CharField(), required=False)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('A user with that username already exists.')
        return value

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email', '')

        user = User.objects.create_user(username=username, email=email, password=password)
        profile_data = {
            'bio': validated_data.get('bio', ''),
            'skills': validated_data.get('skills', []),
            'interests': validated_data.get('interests', []),
            'availability_hours': validated_data.get('availability_hours', 10),
            'preferred_roles': validated_data.get('preferred_roles', []),
        }
        UserProfile.objects.create(user=user, **profile_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            return data
        raise serializers.ValidationError("Both username and password are required!")