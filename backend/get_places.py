import os
import random

import requests
from dotenv import load_dotenv; load_dotenv()

from backend.surprise import Surprise

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
PLACES_URL = "https://places.googleapis.com/v1/places:searchText"
FIELD_MASK = "places.displayName,places.currentOpeningHours,places.googleMapsLinks,places.addressComponents,places.editorialSummary,places.generativeSummary,places.reviewSummary,places.photos,nextPageToken"
PLACES_HEADERS = { 
    "Content-Type": "application/json", 
    "X-Goog-Api-Key": GOOGLE_API_KEY, 
    "X-Goog-FieldMask": FIELD_MASK 
}
GOOGLE_ICON = "https://www.gstatic.com/marketing-cms/assets/images/0f/9a/58f1d92b46069b4a8bdc556b612c/google-maps.webp=s48-fcrop64=1,00000000ffffffff-rw"
RADIUS_MILES = 30
RADIUS_METERS = RADIUS_MILES * 1609.34


def _get_nearby_places(type, zipcode):
    body = {
        "textQuery": f"{type} near {zipcode}",
        # "openNow": "true"
        "minRating": "4.0"
    }
    response = requests.post(PLACES_URL, headers=PLACES_HEADERS, json=body)
    data = response.json()
    places = data["places"]
    while "nextPageToken" in data:
        body["pageToken"] = data["nextPageToken"]
        response = requests.post(PLACES_URL, headers=PLACES_HEADERS, json=body)
        data = response.json()
        for place in data["places"]: places.append(place)
    print(len(places))
    return places


def _get_photo(photo_name):
    photos_url = f"https://places.googleapis.com/v1/{photo_name}/media?maxWidthPx=400&skipHttpRedirect=true&key={GOOGLE_API_KEY}"
    response = requests.get(photos_url)
    data = response.json()
    return data.get("photoUri")


def get_places(type, zipcode):
    pool = _get_nearby_places(type, zipcode)
    places = []
    for _ in range(0, 3):
        place = random.choice(pool)
        pool.remove(place)
        name = place["displayName"]["text"]
        city = None
        hood = None
        for component in place["addressComponents"]:
            if "neighborhood" in component["types"]: hood = component["longText"]
            elif "locality" in component["types"]: city = component["longText"]
        name += f" - {city if hood is None else hood}"
        description = ""
        if "reviewSummary" in place:
            description = " ".join(line.strip() for line in place["reviewSummary"]["text"]["text"].splitlines())
        if "generativeSummary" in place:
            description = place["generativeSummary"]["overview"]["text"] + " (*G*) " + description
        if "editorialSummary" in place:
            description = place["editorialSummary"]["text"] + " (*E*) " + description
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