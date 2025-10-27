from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import  CustomLogin, CustomRgisterView

app_name = 'users'

urlpatterns = [
    # path('registers/', RegisterView.as_view(), name='registers'),
    path('register/', CustomRgisterView.as_view(), name='register'),
    path('login/', CustomLogin.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh-view'),
]
