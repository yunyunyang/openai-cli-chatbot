import json

# Tool schema passed to the model
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "City name"}},
                "required": ["city"],
            },
        },
    }
]


def get_weather(city):
    weather_data = {
        "Taipei": {"temperature": 8, "condition": "Cloudy"},
        "Taoyuan": {"temperature": 15, "condition": "Sunny"},
        "Miaoli": {"temperature": 22, "condition": "Rain"},
    }

    data = weather_data.get(city, {"temperature": "Unknown", "condition": "Unknown"})

    return json.dumps(data, ensure_ascii=False)


# Tool name -> function mapping
tool_functions = {"get_weather": get_weather}
