from django.http import JsonResponse
from .services import fetch_weather_data
from django.http import HttpResponse
from django.shortcuts import render
from .services import get_coordinates


# Function to get weather data for a given city
def weather_data(request, city):
    try:
        # Fetch weather data for the city 
        weather = fetch_weather_data(city)  
        return JsonResponse({'weather': weather})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
def get_forecast(request, location):
    api_key = "dulZUVId8PiZI5WtgxMsgGJgAH6vifyD"  # Your API key
    forecast_data = fetch_weather_data(api_key, location, is_forecast=True)
    
    if forecast_data:
        # Extract relevant data for the 7-day forecast
        forecast_list = []
        for day in forecast_data['timelines']['daily']:
            forecast = {
                'date': day['time'],
                'temp': day['values']['temperature_2m_max'],
                'weather': day['values']['weatherCode'],
            }
            forecast_list.append(forecast)
        
        return JsonResponse(forecast_list, safe=False)
    else:
        return JsonResponse({'error': 'Unable to fetch forecast data'}, status=500)
