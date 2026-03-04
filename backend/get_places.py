import os
import random

import requests
from dotenv import load_dotenv; load_dotenv()

from backend.surprise import Surprise

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
PLACES_URL = "https://places.googleapis.com/v1/places:searchNearby"
FIELD_MASK = "places.displayName,places.currentOpeningHours,places.googleMapsLinks,places.addressComponents,places.reviewSummary,places.photos"
PLACES_HEADERS = { 
    "Content-Type": "application/json", 
    "X-Goog-Api-Key": GOOGLE_API_KEY, 
    "X-Goog-FieldMask": FIELD_MASK 
}
GOOGLE_ICON = "https://www.gstatic.com/marketing-cms/assets/images/0f/9a/58f1d92b46069b4a8bdc556b612c/google-maps.webp=s48-fcrop64=1,00000000ffffffff-rw"
RADIUS_MILES = 20
METERS_PER_MILE = 1609.34


def _get_coordinates(zipcode):
    params = { 
        "address": f"{zipcode}, US", 
        "key": GOOGLE_API_KEY 
    }
    response = requests.get(GEOCODE_URL, params=params)
    data = response.json()
    location = data["results"][0]["geometry"]["location"]
    return location["lat"], location["lng"]


def _get_nearby_places(lat, lng, googlePlaceTypes, radius_meters):
    body = {
        "includedTypes": googlePlaceTypes,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": lat,
                    "longitude": lng,
                },
                "radius": radius_meters,
            }
        }
    }
    response = requests.post(PLACES_URL, headers=PLACES_HEADERS, json=body)
    data = response.json()
    return data.get("places", [])


def _get_photo(photo_name):
    photos_url = f"https://places.googleapis.com/v1/{photo_name}/media?maxWidthPx=400&skipHttpRedirect=true&key={GOOGLE_API_KEY}"
    response = requests.get(photos_url)
    data = response.json()
    return data.get("photoUri")


def get_places(googlePlaceType, zipcode):
    coordinates = _get_coordinates(zipcode)
    pool = _get_nearby_places(lat=coordinates[0], lng=coordinates[1], googlePlaceTypes=[googlePlaceType], radius_meters=(RADIUS_MILES * METERS_PER_MILE))
    places = []
    for _ in range(0, 3):
        place = random.choice(pool)
        name = place["displayName"]["text"]
        city = None
        hood = None
        for component in place["addressComponents"]:
            if "neighborhood" in component["types"]: hood = component["longText"]
            elif "locality" in component["types"]: city = component["longText"]
        name += f" - {city if hood is None else hood}"
        description = " ".join(line.strip() for line in place["reviewSummary"]["text"]["text"].splitlines())
        photos = []
        for i in range(0, len(place["photos"])): 
            photos.append(_get_photo(place["photos"][i]["name"]))
        links = [
            { 
                "href": place["googleMapsLinks"]["placeUri"],
                "src": GOOGLE_ICON
            },
            {
                "href": "",
                "src": "https://www.gstatic.com/marketing-cms/assets/images/ec/00/5d847c1e4109ab4d2d82aec7726f/waze-logo.webp=s48-fcrop64=1,00000000ffffffff-rw"
            }
        ]
        places.append(Surprise(name, description, photos, links))
    return places