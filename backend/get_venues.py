import os
import random
import requests

from dotenv import load_dotenv; load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
PLACES_URL = "https://places.googleapis.com/v1/places:searchNearby"
FIELD_MASK = "places.id,places.displayName,places.location"
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
DRIVE_RADIUS_METERS = 7000   # ~10-min drive
WALK_RADIUS_METERS = 800     # ~10-min walk


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


def get_venues(zipcode):
    coordinates = _get_coordinates(zipcode)
    bars = _search_nearby(lat=coordinates[0], lng=coordinates[1], types=["bar"], radius=DRIVE_RADIUS_METERS)
    bar = random.choice(bars)
    bar_lat = bar["location"]["latitude"]
    bar_lng = bar["location"]["longitude"]
    restaurants = _search_nearby(
        lat=bar_lat,
        lng=bar_lng,
        types=["restaurant"],
        radius=WALK_RADIUS_METERS,
    )
    parks = _search_nearby(
        lat=bar_lat,
        lng=bar_lng,
        types=["park"],
        radius=WALK_RADIUS_METERS,
    )
    if not restaurants or not parks:
        return get_venues(zipcode)
    return {
        "bar": {
            "name": bar["displayName"]["text"],
        },
        "restaurant": {
            "name": random.choice(restaurants)["displayName"]["text"],
        },
        "park": {
            "name": random.choice(parks)["displayName"]["text"],
        },
    }