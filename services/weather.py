import os
from typing import Dict, Any
import requests

OPENWEATHER_API = "https://api.openweathermap.org/data/2.5/weather"

def kelvin_to_celsius(k: float) -> float:
    return round(k - 273.15, 1)

def recommend_activity(main: str, temp_c: float) -> str:
    main_l = (main or '').lower()
    if 'rain' in main_l or 'drizzle' in main_l or 'thunderstorm' in main_l:
        return "It's rainy outside ☔ — watch a movie and have some popcorn!"
    if 'snow' in main_l:
        return "Snowy ❄️ — have a hot tea and take a short walk if possible."
    if 'clear' in main_l:
        if temp_c >= 28:
            return "Clear skies and hot 🔥 — head to the beach or enjoy some ice cream."
        return "Clear skies 🌞 — go for an evening walk or a light run."
    if 'cloud' in main_l:
        return "Cloudy ⛅ — grab a coffee with friends or read a good book at a café."
    if temp_c <= 8:
        return "Very cold 🥶 — drink hot chocolate and watch a good series."
    return "Mild day 🙂 — go for a light walk or hit the gym."

def get_weather_and_activity(city: str) -> Dict[str, Any]:
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        raise RuntimeError("Missing OPENWEATHER_API_KEY in .env file")

    resp = requests.get(OPENWEATHER_API, params={
        "q": city,
        "appid": api_key
    }, timeout=10)

    if resp.status_code != 200:
        try:
            msg = resp.json().get('message', 'Unknown error')
        except Exception:
            msg = resp.text
        raise RuntimeError(f"OpenWeather: {resp.status_code} {msg}")

    payload = resp.json()
    main = payload.get('weather', [{}])[0].get('main', '')
    desc = payload.get('weather', [{}])[0].get('description', '')
    temp_k = payload.get('main', {}).get('temp')
    feels_k = payload.get('main', {}).get('feels_like')
    if temp_k is None:
        raise RuntimeError("Missing temperature in response")

    temp_c = kelvin_to_celsius(temp_k)
    feels_c = kelvin_to_celsius(feels_k) if feels_k is not None else None

    activity = recommend_activity(main, temp_c)

    return {
        "city": payload.get('name', city),
        "country": payload.get('sys', {}).get('country', ''),
        "main": main,
        "description": desc,
        "temp_c": temp_c,
        "feels_c": feels_c,
        "activity": activity,
    }
