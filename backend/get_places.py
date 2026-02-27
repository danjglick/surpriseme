import os
import random
import requests

from dotenv import load_dotenv; load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
PLACES_URL = "https://places.googleapis.com/v1/places:searchNearby"
FIELD_MASK = "places.displayName,places.addressComponents,places.reviewSummary"
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
        place = random.choice(places_pool)
        neighborhood = ""
        for component in place["addressComponents"]:
            if "locality" in component["types"]:
                city = component["longText"]
            elif "neighborhood" in component["types"]:
                neighborhood = component["longText"]
        raw_description = place["reviewSummary"]["text"]["text"]
        description = " ".join(line.strip() for line in raw_description.splitlines())
        disambiguator = f"({city if neighborhood == "" else neighborhood})"
        name = place["displayName"]["text"]
        place = {
            "name": name,
            "disambiguator": disambiguator,
            "description": description
        }
        places.append(place)
    return places