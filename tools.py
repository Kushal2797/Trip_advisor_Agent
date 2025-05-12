import os
import requests
import streamlit as st

GEOAPIFY_KEY = os.getenv("GEOAPIFY_API_KEY")

def get_coordinates(city):
    url = f"https://api.geoapify.com/v1/geocode/search?text={city}&apiKey={GEOAPIFY_KEY}"
    response = requests.get(url).json()

    features = response.get("features", [])
    if not features:
        return {"error": f"❌ City '{city}' not found. Please enter a valid city name."}

    coords = features[0]["geometry"]["coordinates"]
    return {"lat": coords[1], "lon": coords[0]}


@st.cache_data
def get_tourist_spots(lat, lon, radius=5000, limit=5):
    categories = "tourism.attraction,tourism.sights,entertainment.museum,leisure.park,natural"
    url = (
        f"https://api.geoapify.com/v2/places?"
        f"categories={categories}"
        f"&filter=circle:{lon},{lat},{radius}"
        # f"&bias=proximity:{lon},{lat}"
        f"&limit={limit}"
        f"&apiKey={GEOAPIFY_KEY}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        features = response.json().get("features", [])
        spots = []

        for place in features:
            name = place["properties"].get("name", "Unknown place")
            address = place["properties"].get("address_line1", "No address available")
            spot_type = place["properties"].get("category", "Unknown type")
            coords = place["geometry"]["coordinates"]
            spots.append({"name": name, "address": address, "type": spot_type, "coords": coords})

        return spots
    except Exception as e:
        print("Error fetching tourist spots:", e)
        return []

