import json
import requests

# Tool schema passed to the model
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city using Open-Meteo API",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "City name"}},
                "required": ["city"],
            },
        },
    }
]


# Tool implementation
def get_weather(city: str):

    geo_url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={city}&count=1&language=en"
    )

    geo_res = requests.get(geo_url).json()

    if "results" not in geo_res or len(geo_res["results"]) == 0:
        return json.dumps({"error": "city not found"}, ensure_ascii=False)

    location = geo_res["results"][0]
    lat = location["latitude"]
    lon = location["longitude"]
    timezone = location.get("timezone", "auto")

    weather_url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        f"&current=temperature_2m,weather_code"
        f"&timezone={timezone}"
    )

    weather_res = requests.get(weather_url).json()

    current = weather_res.get("current", {})

    result = {
        "city": location["name"],
        "country": location.get("country", ""),
        "latitude": lat,
        "longitude": lon,
        "temperature": current.get("temperature_2m"),
        "weather_code": current.get("weather_code"),
        "timezone": timezone,
    }

    return json.dumps(result, ensure_ascii=False)


# Function mapping
tool_functions = {"get_weather": get_weather}
