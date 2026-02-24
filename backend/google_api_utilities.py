import os
import requests

from dotenv import load_dotenv; load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
PLACES_URL = "https://places.googleapis.com/v1/places:searchNearby"
FIELD_MASK = "places.id,places.displayName,places.location"
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
RADIUS_METERS = 15000   # ~20-min drive


def get_coordinates(zipcode: str):
    params = {
        "address": f"{zipcode}, US",
        "key": GOOGLE_API_KEY
	}
    response = requests.get(GEOCODE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    location = data["results"][0]["geometry"]["location"]
    return location["lat"], location["lng"]
    

def search_nearby(lat, lng, types, radius):
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