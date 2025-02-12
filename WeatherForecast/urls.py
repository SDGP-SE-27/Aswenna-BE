from django.urls import path
from . import views

urlpatterns = [
    # Endpoint to get current weather data
    path('weather/<str:city>/', views.weather_data, name='weather_data'),

    # Endpoint to get 7-day forecast data
    path('WeatherForecast/<str:city>/', views.get_forecast, name='forecast-data'),
]