import streamlit as st
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import random

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Check if API key is loaded
if not API_KEY:
    st.error("API key not found. Make sure to add it to your .env file.")
else:
    # List of background images for different weather conditions
    background_images = {
        "default": "https://i0.wp.com/picjumbo.com/wp-content/uploads/beautiful-fall-nature-scenery-free-image.jpeg?w=600&quality=80",  # Default background
        "hot": "https://img.freepik.com/free-vector/realistic-hot-background_23-2149443988.jpg?semt=ais_hybrid",  # Hot weather background
        "snow": "https://img.freepik.com/premium-photo/cold-weather-serenity-moment-peace_1170794-109141.jpg",  # Snowy background
        "rain": "https://www.wellahealth.com/blog/wp-content/uploads/2021/09/6-ways-to-stay-healthy-during-the-rainy-season.jpg",  # Rainy background
        "clear": "https://cdn2.hubspot.net/hubfs/2936356/maxresdefault.jpg",  # Clear weather background
        "cloudy": "https://www.shutterstock.com/image-photo/rural-landscape-wild-changing-stormy-260nw-1906424227.jpg"  # Cloudy weather background
    }

    # Function to select a background based on weather conditions
    def get_background_image(weather_description, temperature):
        if "rain" in weather_description.lower():
            return background_images["rain"]
        elif "snow" in weather_description.lower():
            return background_images["snow"]
        elif "clear" in weather_description.lower():
            return background_images["clear"]
        elif "cloudy" in weather_description.lower():
            return background_images["cloudy"]
        elif temperature > 30:
            return background_images["hot"]
        else:
            return background_images["default"]  # Default background

    # Custom CSS for Background and UI Styling
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{get_background_image('', 0)}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            font-family: 'Arial', sans-serif;
        }}
        .main-title {{
            color: #ffffff;
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            margin-top: 170px;
        }}
        .recommendation {{
            color: #ffffff;
            font-weight:bold;
            font-size: 30px;
            margin-top: 20px;
        }}
        .card {{
            background: rgba(0, 0, 0, 0.7);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            color: #ffffff;
            text-align: center;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # App Title
    st.markdown('<div class="main-title">Weather App with Recommendations 🌤️</div>', unsafe_allow_html=True)

    # Input for City Name
    # Label with larger text using HTML
    st.markdown('<h2 style="font-size: 25px; margin-top: 10px;color: #ffffff;">Enter your city name:</h2>', unsafe_allow_html=True)


# City name input
    city_name = st.text_input(" ", placeholder="e.g., MUMBAI , DELHI , IN")


    if city_name:
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": city_name,
            "appid": API_KEY,
            "units": "metric"  # Metric for Celsius, 'imperial' for Fahrenheit
        }

        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()

            # Extract Data
            weather = data['weather'][0]['description'].capitalize()
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            country = data['sys']['country']

            # Update background based on weather conditions
            background_url = get_background_image(weather, temperature)

            # Update CSS for background
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("{background_url}");
                }}
                </style>
                """,
                unsafe_allow_html=True,
            )

            # Display Weather Info
            st.markdown(
                f"""
                <div class="card">
                    <h2 style="color:white;">{city_name}, {country}</h2>
                    <p><b>Weather:</b> {weather}</p>
                    <p><b>Temperature:</b> {temperature}°C</p>
                    <p><b>Humidity:</b> {humidity}%</p>
                    <p><b>Wind Speed:</b> {wind_speed} m/s</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Provide Recommendations
            recommendation = ""

            if "rain" in weather.lower():
                recommendation = "It's rainy outside. Don't forget to carry an umbrella! ☔ Also, wearing waterproof clothing would be advisable."
            elif temperature > 30:
                recommendation = "It's quite hot. Stay hydrated and avoid outdoor activities during peak hours. 🥤 Consider wearing light and breathable fabrics like cotton or linen."
            elif temperature < 10:
                recommendation = "It's cold. Wear warm clothes if you're heading out! 🧣 A coat or thermal wear could help."
            elif "snow" in weather.lower():
                recommendation = "It's snowy outside. Make sure to wear heavy and insulated clothing. 🧥 Boots and a warm hat would be beneficial."
            elif "clear" in weather.lower():
                recommendation = "The weather looks pleasant. Enjoy your day! 🌤️ Consider wearing casual or semi-formal attire if you're heading out."
            elif "cloudy" in weather.lower():
                recommendation = "It’s cloudy today. A sweater or long-sleeve shirt would be comfortable. 🧥"
            else:
                recommendation = "The weather conditions are neutral. Dress comfortably."

            # Display the recommendation
            st.markdown(f'<div class="recommendation">{recommendation}</div>', unsafe_allow_html=True)

        else:
            st.error("City not found. Please check the spelling or try a different city.")

    # Footer
    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px; color: #ffffff;">
            Developed with ❤️ using Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )
