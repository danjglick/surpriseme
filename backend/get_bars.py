import os
import random
import requests

from dotenv import load_dotenv; load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
PLACES_URL = "https://places.googleapis.com/v1/places:searchNearby"
FIELD_MASK = "places.id,places.displayName,places.location"
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
DRIVE_RADIUS_METERS = 15000   # ~10-min drive


def _get_coordinates(zipcode: str = "02128", country="US"):
    params = {
        "address": f"{zipcode}, {country}",
        "key": GOOGLE_API_KEY
	}
    response = requests.get(GEOCODE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    location = data["results"][0]["geometry"]["location"]
    return location["lat"], location["lng"]
    

def _search_nearby(lat, lng, types, radius):
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": FIELD_MASK,
    }
    body = {
        "includedTypes": types,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": lat,
                    "longitude": lng,
                },
                "radius": radius,
            }
        },
    }
    response = requests.post(PLACES_URL, headers=headers, json=body)
    data = response.json()
    return data.get("places", [])


def get_bars(zipcode):
    coordinates = _get_coordinates(zipcode)
    valid_bars = _search_nearby(lat=coordinates[0], lng=coordinates[1], types=["bar"], radius=DRIVE_RADIUS_METERS)
    selected_bars = []
    for _ in range(0, 3):
        selected_bars.append(random.choice(valid_bars)["displayName"]["text"])
    return selected_bars