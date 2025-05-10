import requests
import os
from dotenv import load_dotenv
load_dotenv()

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

def get_coordinates(city_name: str) -> str:
    url = f"https://api.geoapify.com/v1/geocode/search?text={city_name}&apiKey={GEOAPIFY_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data['features']:
        coords = data['features'][0]['geometry']['coordinates']
        return f"{coords[1]}, {coords[0]}"  # lat, lon
    return "Coordinates not found"

def get_tourist_spots(lat: float, lon: float, radius=1000, limit=10) -> str:
    url = (
        f"https://api.geoapify.com/v2/places?categories=tourism.attraction&"
        f"filter=circle:{lon},{lat},{radius}&limit={limit}&apiKey={GEOAPIFY_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()
    spots = []
    for place in data.get("features", []):
        props = place["properties"]
        name = props.get("name", "Unknown")
        address = props.get("address_line1", "")
        spots.append(f"{name} - {address}")
    return "\n".join(spots) if spots else "No tourist attractions found."
