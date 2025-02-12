from django.urls import path
from .views import ProtectedEndpointView, UserRegistrationView, UserLoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView




urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),  # ✅ Register user
    path('login/', UserLoginView.as_view(), name='login'),   # ✅ Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]



