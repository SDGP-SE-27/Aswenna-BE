import requests
from supabase import create_client
from django.conf import settings

GEOCODE_API_KEY = '35838cc8ed1349c7ae424f795d5f404e'

# Function to fetch coordinates (latitude, longitude) for a given city
def get_coordinates(city: str):
    # Construct the geocoding API URL
    url = f'https://api.opencagedata.com/geocode/v1/json?q={city}&key={GEOCODE_API_KEY}'
    
    try:
        # Make a request to OpenCage Geocoding API
        response = requests.get(url)
        data = response.json()

        # Check if the API returned a result
        if data['results']:
            # Extract latitude and longitude from the API response
            lat = data['results'][0]['geometry']['lat']
            lon = data['results'][0]['geometry']['lng']
            return lat, lon
        else:
            print(f"No geocoding results found for city: {city}")
            return None, None  # Return None if no results are found

    except Exception as e:
        print(f"Error fetching geocode for city {city}: {e}")
        return None, None  # Return None if there's an error



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
    api_key = 'dulZUVId8PiZI5WtgxMsgGJgAH6vifyD'
    weather_data_list = []  # To store weather data for all cities

    for city in cities:
        location_coords = get_coordinates(city)  # Get coordinates (lat, lon) for the city
        if location_coords[0] is None or location_coords[1] is None:
            continue  # Skip the city if coordinates couldn't be fetched
        url = f'https://api.tomorrow.io/v4/timelines?location={location_coords[0]},{location_coords[1]}&fields=temperature,weatherCode,windSpeed,humidity&timesteps=current&apikey={api_key}'

        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            # Extract necessary data from the response
            current_weather = data['data']['timelines'][0]['intervals'][0]['values']
            weather_code = current_weather['weatherCode']
            weather_description = weather_code_map.get(weather_code, 'Sunny')  # Default to 'Sunny' if code not found

            weather_data = {
                'city': city,
                'temperature': current_weather['temperature'],
                'humidity': current_weather['humidity'],
                'description': weather_description,
                'wind_speed': current_weather['windSpeed'],
            }
            
            # Save the weather data to the Supabase database
            supabase.table('weather_data').insert(weather_data).execute()
            
            weather_data_list.append(weather_data)  # Add data to the list

    return weather_data_list

