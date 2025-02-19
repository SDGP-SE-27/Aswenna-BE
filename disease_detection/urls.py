# disease_detection/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('predict/banana/', views.predict_banana, name='predict_banana'),
    path('predict/mango/', views.predict_mango, name='predict_mango'),
    path('predict/papaya/', views.predict_papaya, name='predict_papaya'),
    path('predict/snake_gourd/', views.predict_snake_gourd, name='predict_snake_gourd'),
    path('predict/eggplant/', views.predict_eggplant, name='predict_eggplant'),
    path('predict/okra/', views.predict_okra, name='predict_okra'),

]