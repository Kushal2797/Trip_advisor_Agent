import os
import requests

GEOAPIFY_KEY = os.getenv("GEOAPIFY_API_KEY")

def get_coordinates(city: str):
    url = f"https://api.geoapify.com/v1/geocode/search?text={city}&apiKey={GEOAPIFY_KEY}"
    res = requests.get(url).json()
    feature = res['features'][0]['geometry']['coordinates']
    return {"lon": feature[0], "lat": feature[1]}

def get_tourist_spots(lat, lon):
    url = f"https://api.geoapify.com/v2/places?categories=tourism.attraction&filter=circle:{lon},{lat},3000&limit=10&apiKey={GEOAPIFY_KEY}"
    res = requests.get(url).json()
    places = [f"{p['properties']['name']} ({p['properties'].get('address_line1', 'No address')})" for p in res['features']]
    return places or ["No tourist attractions found."]
