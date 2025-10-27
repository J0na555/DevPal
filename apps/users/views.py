from rest_framework import generics, permissions, status
from .serializers import RegisterSerializer, LoginSerializer
from .models import UserProfile
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect

# class RegisterView(generics.CreateAPIView):
#     serializer_class = RegisterSerializer
#     permission_classes = [permissions.AllowAny]


class CustomRgisterView(generics.GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    template_name = 'users/register.html'
    context_object_name = 'user-registration'

    def post(self, request):
        pass
    


class CustomLogin(generics.GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    template_name = 'users/login.html'
    context_object_name = 'user-login'

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            from .serializers import UserProfileSerializer
            profile_serializer = UserProfileSerializer(user.userprofile)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'profile': profile_serializer.data
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

