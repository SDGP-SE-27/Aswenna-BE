from django.urls import path
from .views import ProtectedEndpointView, UserRegistrationView, UserLoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView




urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),  # ✅ Register user
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # ✅ Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]



