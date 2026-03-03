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
    "X-Goog-FieldMask": FIELD_MASK,
}
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


def _search_nearby(lat, lng, googlePlaceTypes, radius_meters):
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


def get_places(googlePlaceType, zipcode="02128"):
    coordinates = _get_coordinates(zipcode)
    places_pool = _search_nearby(lat=coordinates[0], lng=coordinates[1], googlePlaceTypes=[googlePlaceType], radius_meters=(RADIUS_MILES * METERS_PER_MILE))
    places = []
    for _ in range(0, 3):
        place = random.choice(places_pool)
        name = place["displayName"]["text"]
        city = None
        neighborhood = None
        for component in place["addressComponents"]:
            if "neighborhood" in component["types"]:
                neighborhood = component["longText"]
            elif "locality" in component["types"]:
                city = component["longText"]
        locale = city if neighborhood is None else neighborhood
        name += f" - {locale}"
        # is_open_now = place["currentOpeningHours"]["openNow"]
        maps_link = place["googleMapsLinks"]["placeUri"]
        links = [maps_link]
        description = " ".join(line.strip() for line in place["reviewSummary"]["text"]["text"].splitlines())
        photo = None
        if place.get("photos"):
            photo_name = place["photos"][0]["name"]
            photo = _get_photo(photo_name)
        place = Surprise(name, description, photo, links)
        places.append(place)
    return places