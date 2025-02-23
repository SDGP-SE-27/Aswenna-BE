from django.urls import path
from . import views

urlpatterns = [
    path('<str:crop>/', views.crop, name='crop_data'),  # Use a dynamic parameter for crop name
]
