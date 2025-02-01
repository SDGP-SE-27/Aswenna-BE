from django.urls import path
from .views import create_farmland

urlpatterns = [
    path('create/', create_farmland, name='create_farmland'),
]
