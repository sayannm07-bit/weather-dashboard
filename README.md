Weather Dashboard

A command-line weather dashboard using only Python's built-in libraries. It finds a city and retrieves current weather from Open-Meteo. No API key or third-party package is required.

Features : 
Modular WeatherAPIClient class
City search and coordinate lookup
Temperature, feels-like temperature, humidity, wind speed, precipitation, and conditions
JSON response parsing
Friendly handling of unknown cities, HTTP errors, timeouts, and connection failures
Uses urllib, json, and other standard-library modules

Requirements : 
Python 3.9 or newer recommended
No external packages

Run : 
Open a terminal in this folder and run:
python main.py
Enter a city name when prompted, for example Delhi, Mumbai, or London.

API Configuration : 
The program uses:
Open-Meteo Geocoding API: https://geocoding-api.open-meteo.com/v1/search
Open-Meteo Forecast API: https://api.open-meteo.com/v1/forecast
These example endpoints do not require an API key. An internet connection is required. Since no secret is used, you do not need a .env file or API credential.

Example Output :
The numbers and condition vary with the live response.
CodeNova Weather Dashboard (Open-Meteo; no API key required)
Enter a city name: Delhi

========== WEATHER DASHBOARD ==========
City: Delhi
Conditions: Mainly clear
Temperature: <live value> °C
Feels like: <live value> °C
Humidity: <live value> %
Wind speed: <live value> km/h
Precipitation: <live value> mm
=======================================
Values in angle brackets are illustrative placeholders, not actual current readings.

Test Cases : 
Valid city: enter Delhi and confirm weather metrics appear when online.
Invalid city: enter a made-up name and check the friendly not-found message.
Offline: disable internet and confirm a connection error is shown instead of an unhandled traceback.
Timeout: try on a slow network to exercise timeout handling.

Project Files : 
main.py — application and API client class
README.md — instructions and test cases

Limitations : 
This is a terminal-based dashboard. It needs internet access for current weather, and the result depends on the public API. No live API query is included in the example output.

Learning Outcomes : 
Practise modular classes, HTTP requests with urllib, URL encoding, JSON parsing, and exception handling.