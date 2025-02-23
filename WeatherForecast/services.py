import requests 
from supabase import create_client
from django.conf import settings

GEOCODE_API_KEY = settings.OPENCAGE_API_KEY
YOUR_API_KEY = settings.TOMORROW_API_KEY

# Function to fetch coordinates (latitude, longitude) for a given city
def get_coordinates(city: str):
    # Construct the geocoding API URL
    url = f'https://api.opencagedata.com/geocode/v1/json?q={city}&key={GEOCODE_API_KEY}'
    print(f"Geocoding URL: {url}")  # Debugging

    try:
        # Make a request to OpenCage Geocoding API
        response = requests.get(url, timeout=10)
        data = response.json()
        print(f"Geocoding API response: {data}") #Debugging

        # Check if the API returned a result
        if data['results']:
            # Extract latitude and longitude from the API response
            lat = data['results'][0]['geometry']['lat']
            lon = data['results'][0]['geometry']['lng']
            print(f"Geocoding API Success: {lat, lon}")
            return lat, lon
        else:
            print(f"No geocoding results found for city: {city}")
            return None, None  # Return None if no results are found

    except requests.exceptions.Timeout:
        print(f"Geocode request timed out for city: {city}")
        return None, None  # Return None if there's a timeout error

    except requests.exceptions.RequestException as e:
        print(f"Error fetching geocode for city {city}: {e}")
        return None, None  # Return None if there's a network error



# Create the Supabase client
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_API_KEY)

# List of cities in Western and Southern provinces
cities = [
    'Colombo', 'Gampaha', 'Kalutara', 'Negombo',  # Western Province
    'Galle', 'Matara', 'Hambantota', 'Ambalangoda'  # Southern Province
]

# Weather code mapping to readable description
weather_code_map = {
    'clear-day': 'Clear Day',
    'sunny': 'Sunny',
    'cloudy': 'Cloudy',
    'partly-cloudy-day': 'Partly Cloudy',
    'heavy-showers': 'Heavy Showers',
    'thunderstorm': 'Thunderstorm',
}

# Function to fetch weather data for multiple cities
def fetch_weather_data(city):
    location_coords = get_coordinates(city)
    if location_coords[0] is None or location_coords[1] is None:
        print(f"Could not retreive coords from {city}")
        return None  # Return None if coordinates couldn't be fetched
    
    lat, lon = location_coords
    current_url = f'https://api.tomorrow.io/v4/timelines?location={lat},{lon}&fields=temperature,weatherCode,windSpeed,humidity&timesteps=current&apikey={YOUR_API_KEY}'
    print(f"Weather API CALL: {current_url}")

    try:
        current_response = requests.get(current_url)
        current_data = current_response.json()
        print(f"Weather API response: {current_data}")

        forecast_url = f'https://api.tomorrow.io/v4/timelines?location={lat},{lon}&fields=temperature,weatherCode,windSpeed,humidity&timesteps=1d&apikey={YOUR_API_KEY}'
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        if current_response.status_code == 200 and forecast_response.status_code == 200:
            weather_data = current_data['data']['timelines'][0]['intervals'][0]['values']
            forecast_data_list = []
            for day in forecast_data['data']['timelines'][0]['intervals']:
                weather_code = day['values']['weatherCode']
                weather_description = weather_code_map.get(weather_code, 'Sunny')
                forecast = {
                    'date': day['startTime'],
                    'temp': day['values']['temperature'],
                    'weather': weather_description,
                }
                forecast_data_list.append(forecast)
            return {
                'weather': {
                    'city': city,
                    'temperature': weather_data['temperature'],
                    'humidity': weather_data['humidity'],
                    'description': weather_description,
                    'wind_speed': weather_data.get('windSpeed', 'N/A'),
                },
                'forecast': forecast_data_list
            }
        else:
            print(f"Error fetching weather data: {current_response.status_code}")
            return None  # Return None if the response status is not 200
    except requests.exceptions.Timeout:
        print(f"Weather request timed out for city: {city}")
        return None  # Return None in case of a timeout

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None  # Return None in case of a network error


def fetch_forecast_data(city):
    location_coords = get_coordinates(city)
    if location_coords[0] is None or location_coords[1] is None:
        print(f"Could not retrieve coordinates for {city}")
        return None  # Return None if coordinates couldn't be fetched
    
    lat, lon = location_coords
    url = f'https://api.tomorrow.io/v4/timelines?location={lat},{lon}&fields=temperature,weatherCode,windSpeed,humidity&timesteps=1d&apikey={YOUR_API_KEY}'
    print(f"Forecast API Call: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        print(f"Forecast API response: {data}")

        if response.status_code == 200:
            forecast_data = data['data']['timelines'][0]['intervals']
            forecast_list = []
            for day in forecast_data:
                weather_code = day['values']['weatherCode']
                weather_description = weather_code_map.get(weather_code, 'Sunny')  # Default to 'Sunny'
                forecast = {
                    'date': day['startTime'],
                    'temp': day['values']['temperature'],
                    'weather': weather_description,
                }
                forecast_list.append(forecast)
            return {
                'weather': {
                    'city': city,
                    'temperature': forecast_data['temperature'],
                    'humidity': forecast_data['humidity'],
                    'description': weather_description,
                    'wind_speed': forecast_data.get('windSpeed', 'N/A'),
                },
                'forecast': forecast_list,
            }
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            return None  # Return None if the response is not successful

    except requests.exceptions.Timeout:
        print(f"Forecast request timed out for city: {city}")
        return None  # Return None in case of a timeout

    except requests.exceptions.RequestException as e:
        print(f"Error fetching forecast data: {e}")
        return None  # Return None in case of a network error