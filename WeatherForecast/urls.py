# from django.urls import path
# from . import views

# urlpatterns = [
#     # Endpoint to get current weather data
#     path('weather/<str:city>/', views.WeatherData.as_view(), name='weather_data'),

#     # Endpoint to get 7-day forecast data
#     path('forecast/<str:city>/', views.ForecastData.as_view(), name='forecast_data'),
# ]

from django.urls import path
from .views import WeatherData, ForecastData

urlpatterns = [
    path('weather/<str:city>/', WeatherData.as_view(), name='weather-data'),
    path('forecast/<str:city>/', ForecastData.as_view(), name='forecast-data'),  # Ensure it uses `city`
]
