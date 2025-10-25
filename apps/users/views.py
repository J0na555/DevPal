from django.shortcuts import render
from .serializers import UserSerializer
from .models import UserProfile
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

class TokenObtainView(TokenObtainPairView):
    serializer_class = UserSerializer

