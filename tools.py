def calculator(a: float, b: float, operation: str):
    """Perform a basic mathematical calculation."""

    if operation == "add":
        return a + b

    elif operation == "substract":
        return a - b

    elif operation == "multiply":
        return a * b

    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    else:
        raise ValueError(f"Unsupported operation: {operation}")

def get_weather(city: str):
    """Get weather information for a city."""

    wheather_data = {
        "Delhi": "32 C, Sunny",
        "Mumbai": "29 C, Cloudy",
        "Bangalore": "24 C, Rainy"
    }

    return wheather_data.get(
        city,
        "Weather data not available"
    )