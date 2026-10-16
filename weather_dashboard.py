
import requests
class WeatherAPIClient:
    """Fetch location coordinates and current weather from Open-Meteo."""

    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, timeout=10):
        self.timeout = timeout
        self.session = requests.Session()

    def find_city(self, city):
        try:
            response = self.session.get(
                self.GEOCODING_URL,
                params={"name": city, "count": 1, "language": "en", "format": "json"},
                timeout=self.timeout,
            )
            response.raise_for_status()
            results = response.json().get("results", [])
        except requests.exceptions.Timeout as exc:
            raise RuntimeError("The location search timed out. Please try again.") from exc
        except requests.exceptions.ConnectionError as exc:
            raise RuntimeError("Could not connect. Check your internet connection.") from exc
        except requests.exceptions.HTTPError as exc:
            raise RuntimeError("The location service returned an HTTP error.") from exc
        except (ValueError, requests.exceptions.RequestException) as exc:
            raise RuntimeError("Could not read the location service response.") from exc

        if not results:
            raise ValueError(f"No matching city found for '{city}'. Check the spelling.")
        return results[0]

    def get_current_weather(self, latitude, longitude):
        try:
            response = self.session.get(
                self.WEATHER_URL,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "temperature_2m,relative_humidity_2m,apparent_temperature,"
                               "is_day,precipitation,weather_code,wind_speed_10m",
                    "timezone": "auto",
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.Timeout as exc:
            raise RuntimeError("The weather request timed out. Please try again.") from exc
        except requests.exceptions.ConnectionError as exc:
            raise RuntimeError("No internet connection detected. Please check your network.") from exc
        except requests.exceptions.HTTPError as exc:
            raise RuntimeError(f"Weather service HTTP error ({response.status_code}).") from exc
        except (ValueError, requests.exceptions.RequestException) as exc:
            raise RuntimeError("Could not read the weather service response.") from exc

        current = data.get("current")
        if not isinstance(current, dict):
            raise RuntimeError("The weather service did not return current weather data.")
        return current


def describe_weather(code):
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail",
    }
    try:
        return descriptions.get(int(code), "Unknown conditions")
    except (TypeError, ValueError):
        return "Unknown conditions"


def show_weather(city, location, current):
    units = current.get("units", {})
    print("\n========== WEATHER DASHBOARD ==========")
    print(f"City: {location.get('name', city)}")
    area = ", ".join(
        part for part in [location.get("admin1"), location.get("country")] if part
    )
    if area:
        print(f"Region: {area}")
    print(f"Updated: {current.get('time', 'Not available')}")
    print(f"Conditions: {describe_weather(current.get('weather_code'))}")
    print(f"Temperature: {current.get('temperature_2m', 'N/A')} "
          f"{units.get('temperature_2m', '°C')}")
    print(f"Feels like: {current.get('apparent_temperature', 'N/A')} "
          f"{units.get('apparent_temperature', '°C')}")
    print(f"Humidity: {current.get('relative_humidity_2m', 'N/A')} "
          f"{units.get('relative_humidity_2m', '%')}")
    print(f"Wind speed: {current.get('wind_speed_10m', 'N/A')} "
          f"{units.get('wind_speed_10m', 'km/h')}")
    print(f"Precipitation: {current.get('precipitation', 'N/A')} "
          f"{units.get('precipitation', 'mm')}")
    print("=======================================\n")


def main():
    print("CodeNova Weather Dashboard (Open-Meteo; no API key required)")
    city = input("Enter a city name: ").strip()
    if not city:
        print("Please enter a city name.")
        return

    client = WeatherAPIClient()
    try:
        location = client.find_city(city)
        current = client.get_current_weather(location["latitude"], location["longitude"])
        show_weather(city, location, current)
    except ValueError as error:
        print(f"Location error: {error}")
    except RuntimeError as error:
        print(f"Weather error: {error}")
    except (KeyError, TypeError) as error:
        print(f"Unexpected response format from weather service: {error}")


if __name__ == "__main__":
    main()
