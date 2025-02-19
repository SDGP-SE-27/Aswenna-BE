# from django.http import JsonResponse
# from .services import fetch_weather_data, fetch_forecast_data
# from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.views import APIView
# from rest_framework.response import Response


# @api_view(['GET'], 
# authentication_classes=[TokenAuthentication], 
# permission_classes=[AllowAny])
# def get_weather_data(request, city):
#     try:
#         # Fetch weather data for the city 
#         weather = fetch_weather_data(city)
        
#         if weather:
#             return JsonResponse({'weather': weather})
#         else:
#             return JsonResponse({'error': 'No weather data found'}, status=400)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)

#@api_view(['GET'])
#def get_forecast(request, city):
    # try:
    #     # Fetch forecast data for the city
    #     forecast_data = fetch_forecast_data(city)  # Ensure this function is properly defined
        
    #     if forecast_data:
    #         return JsonResponse({'forecast': forecast_data})
    #     else:
    #         return JsonResponse({'error': 'No forecast data found'}, status=400)
    # except Exception as e:
    #     return JsonResponse({'error': str(e)}, status=400)

#

#

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from .services import fetch_weather_data, fetch_forecast_data

class WeatherData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, city):  # Automatically receives 'city' from URL
        print(f"WeatherData view called for city: {city}")  # Debugging
        try:
            weather = fetch_weather_data(city)
            if weather:
                print(f"WeatherData returned: {weather}")  # Debugging
                return Response({'weather': weather})
            else:
                print("WeatherData: No weather data found")  # Debugging
                return Response({'error': 'No weather data found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class ForecastData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, city):  # Automatically receives 'city' from URL
        print(f"ForecastData view called for city: {city}")  # Debugging
        try:
            forecast_data = fetch_forecast_data(city)
            if forecast_data:
                print(f"ForecastData returned: {forecast_data}")  # Debugging
                return Response(forecast_data)
            else:
                print("ForecastData: No forecast data found")  # Debugging
                return Response({'error': 'No forecast data found'}, status=400)
        except Exception as e:
            print(f"ForecastData error: {str(e)}")  # Debugging
            return Response({'error': str(e)}, status=400)

