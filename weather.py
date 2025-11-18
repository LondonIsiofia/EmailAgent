import requests
from config import OPENWEATHER_API_KEY, IPINFO_URL

def detect_location():
    try:
        r = requests.get(IPINFO_URL, timeout=6)
        r.raise_for_status()
        data = r.json()
        city = data.get("city", "")
        country = data.get("country", "")
        region = data.get("region", "")
        loc = {"city": city, "region": region, "country": country}
        return loc
    except Exception as e:
        print(f"[location] Error detecting location: {e}")
        return {"city": "", "region": "", "country": ""}

    
def get_weather_for_location(city: str, country_code: str):
    if not OPENWEATHER_API_KEY or not city:
        return "🌤 Weather: (not available - API key or location missing)"
    q = f"{city}, {country_code}" if country_code else city
    url = f"https://api.openweathermap.org/data/2.5/weather?q={q}&appid={OPENWEATHER_API_KEY}&units=imperial"
    try:
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        d = r.json()
        temp = d["main"]["temp"]
        cond = d["weather"][0]["description"].capitalize()
        wind = d["wind"].get("speed", None)
        humid = d["main"].get("humidity", None)
        return f"🌤 Weather — {city}, {country_code}: {temp:.0f}°F, {cond}. Wind: {wind} mph. Humidity: {humid}%"
    except Exception as e:
        return f"🌤 Weather: (error fetching: {e})"
    
def get_auto_weather():
    loc = detect_location()
    city = loc.get("city") or ""
    country = loc.get("country") or ""
    return get_weather_for_location(city, country)