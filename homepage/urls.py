from django.urls import path
from .views import get_user_farmland
from .views import get_user_details
from .views import reset_password


urlpatterns = [
    path('farmland/<str:username>/', get_user_farmland, name='get_user_farmland'),
    path('user-details/', get_user_details, name='get_user_details'),
    path('reset-password/', reset_password, name='reset_password'),
   
]



