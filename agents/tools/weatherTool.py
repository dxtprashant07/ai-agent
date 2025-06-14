import os
import requests
from dotenv import load_dotenv

load_dotenv()

class WeatherTool:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city):
        if not self.api_key:
            return "OpenWeatherMap API key not found. Please set OPENWEATHER_API_KEY in your .env file."
        
        try:
            url = f"{self.base_url}?q={city}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if data.get('cod') != 200:
                return f"Weather API error: {data.get('message', 'Unknown error')}"
            
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind = data['wind']['speed']
            
            return (f"The temperature in {city.title()} is {temp}°C with {desc}.\n"
                   f"Humidity: {humidity}%\nWind Speed: {wind} m/s")
        except Exception as e:
            return f"Weather API error: {str(e)}"