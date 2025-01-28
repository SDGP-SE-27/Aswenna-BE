from django.urls import path
from .views import ProtectedEndpointView, UserRegistrationView, UserLoginView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('protected-endpoint/', ProtectedEndpointView.as_view(), name='protected-endpoint'),
]
