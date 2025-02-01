from django.urls import path
from .views import get_user_farmland

urlpatterns = [
    path('farmland/<str:username>/', get_user_farmland, name='get_user_farmland'),
]



