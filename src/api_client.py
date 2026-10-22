import requests

class AirportApiClient:
    def __init__(self):
        self.url = "https://raw.githubusercontent.com/jbrooksuk/JSON-Airports/refs/heads/master/airports.json"


    def fetch_airports(self):
        response = requests.get(self.url, timeout=30)
        response.raise_for_status()
        return response.json()