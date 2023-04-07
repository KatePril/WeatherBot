import requests
from decouple import config

api_key = config('WEATHER_API_KEY')

def get_weather(city):
    global api_key
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
    weather_data = response.json()
    if weather_data['cod'] == '404':
        return "There is no such city"
    else:
        weather_description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        temp_feels_like = weather_data['main']['feels_like']
        temp_min = weather_data['main']['temp_min']
        temp_max = weather_data['main']['temp_max']
        visibility = weather_data['visibility']
        wind_speed = weather_data['wind']['speed']
        return f"Weather description: {weather_description}\nAvarage temperature: {temperature}°C\nFeels like: {temp_feels_like}°C\nMinim temperature: {temp_min}°C\nMaximum temperature: {temp_max}°C\nVisibility: {visibility} nephelometers\nSpeed of the wind: {wind_speed}"