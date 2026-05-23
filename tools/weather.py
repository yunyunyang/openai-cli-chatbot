import json
import requests

# Tool schema passed to the model
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather using Open-Meteo API",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_wttr_weather",
            "description": "Get weather using wttr.in simple text API",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"],
            },
        },
    },
]


# Tool implementation
def get_weather(city: str):
    print("==== get_weather ====")
    geo_url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={city}&count=1&language=en"
    )

    geo_res = requests.get(geo_url, timeout=5).json()

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

    try:
        weather_res = requests.get(weather_url, timeout=5).json()
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

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


def get_wttr_weather(city: str):
    url = f"https://wttr.in/{city}"

    res = requests.get(url, timeout=5)

    if res.status_code == 200:
        print(res.text)
        return res.text
    else:
        print("error:", res.status_code)
        return None


# Function mapping
tool_functions = {"get_weather": get_weather, "get_wttr_weather": get_wttr_weather}
