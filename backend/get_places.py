import os
import random
import requests

from dotenv import load_dotenv; load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
PLACES_URL = "https://places.googleapis.com/v1/places:searchNearby"
FIELD_MASK = "places.id,places.displayName,places.location"
RADIUS_MILES = 20
RADIUS_METERS = RADIUS_MILES * 1609.34


def _get_coordinates(zipcode: str):
    params = {
        "address": f"{zipcode}, US",
        "key": GOOGLE_API_KEY
	}
    response = requests.get(GEOCODE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    location = data["results"][0]["geometry"]["location"]
    return location["lat"], location["lng"]
    

def _search_nearby(latitude, longitude, types, radius):
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
                    "latitude": latitude,
                    "longitude": longitude,
                },
                "radius": radius,
            }
        },
    }
    response = requests.post(PLACES_URL, headers=headers, json=body)
    data = response.json()
    return data.get("places", []) 


def get_places(googlePlaceType: str, zipcode: str = "02128"):
    coordinates = _get_coordinates(zipcode)
    places_pool = _search_nearby(latitude=coordinates[0], longitude=coordinates[1], types=[googlePlaceType], radius=RADIUS_METERS)
    places = []
    for _ in range(0, 3):
        places.append(random.choice(places_pool)["displayName"]["text"])
    return places
