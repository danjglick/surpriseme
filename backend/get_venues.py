import os
import requests
import random

from dotenv import load_dotenv; load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("WARNING: GOOGLE_API_KEY not set!")
else:
    print(f"API Key loaded: {GOOGLE_API_KEY[:10]}...")  # Show first 10 chars
ZIP_CENTER = {"lat": 42.3782, "lng": -71.0325}
DRIVE_RADIUS_METERS = 7000   # ~10-min drive
WALK_RADIUS_METERS = 800     # ~10-min walk
PLACES_URL = "https://places.googleapis.com/v1/places:searchNearby"
FIELD_MASK = "places.id,places.displayName,places.location"


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
    res = requests.post(PLACES_URL, headers=headers, json=body)
    if not res.ok:
        raise RuntimeError(f"Places API error: {res.status_code} {res.text}")
    data = res.json()
    return data.get("places", [])


def random_pick(arr):
    return random.choice(arr)


def get_venues():
    bars = search_nearby(
        lat=ZIP_CENTER["lat"],
        lng=ZIP_CENTER["lng"],
        types=["bar"],
        radius=DRIVE_RADIUS_METERS,
    )
    if not bars:
        raise RuntimeError("No bars found")
    bar = random_pick(bars)
    bar_lat = bar["location"]["latitude"]
    bar_lng = bar["location"]["longitude"]
    restaurants = search_nearby(
        lat=bar_lat,
        lng=bar_lng,
        types=["restaurant"],
        radius=WALK_RADIUS_METERS,
    )
    parks = search_nearby(
        lat=bar_lat,
        lng=bar_lng,
        types=["park"],
        radius=WALK_RADIUS_METERS,
    )
    if not restaurants or not parks:
        return get_venues()
    return {
        "bar": {
            "name": bar["displayName"]["text"],
        },
        "restaurant": {
            "name": random_pick(restaurants)["displayName"]["text"],
        },
        "park": {
            "name": random_pick(parks)["displayName"]["text"],
        },
    }