import os
import random

from dotenv import load_dotenv; load_dotenv()
import requests

from backend.surprise import Surprise

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
PLACES_URL = "https://places.googleapis.com/v1/places:searchText"
FIELD_MASK = "places.displayName,places.currentOpeningHours,places.googleMapsLinks,places.addressComponents,places.editorialSummary,places.reviewSummary,places.photos,nextPageToken"
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
        "minRating": "4.0",
        # "openNow": "true"
    }
    response = requests.post(PLACES_URL, headers=PLACES_HEADERS, json=body)
    data = response.json()
    places = data["places"]
    while "nextPageToken" in data:
        body["pageToken"] = data["nextPageToken"]
        response = requests.post(PLACES_URL, headers=PLACES_HEADERS, json=body)
        data = response.json()
        for place in data["places"]: 
            places.append(place)
    return places


def _get_name(place):
    name = place["displayName"]["text"]
    city = None
    hood = None
    for component in place["addressComponents"]:
        if "neighborhood" in component["types"]: 
            hood = component["longText"]
        elif "locality" in component["types"]: 
            city = component["longText"]
    locale = city if hood is None else hood
    name += f" - {locale}"
    return name


def _get_description(place):
    description = None
    if "reviewSummary" in place:
        description = place["reviewSummary"]["text"]["text"]
        description = " ".join(line.strip() for line in description.splitlines())
    elif "editorialSummary" in place:
        description = place["editorialSummary"]["text"]
    return description


def _get_photos(place):
    photos = []
    for i in range(0, len(place["photos"])):
        photo_name = place["photos"][i]["name"]
        photos_url = f"https://places.googleapis.com/v1/{photo_name}/media?maxWidthPx=400&skipHttpRedirect=true&key={GOOGLE_API_KEY}"
        response = requests.get(photos_url)
        data = response.json()
        photo = data.get("photoUri")
        photos.append(photo)
    return photos


def _get_links(place):
    return [
        { 
            "href": place["googleMapsLinks"]["placeUri"],
            "src": GOOGLE_ICON
        },
        {
            "href": "",
            "src": "https://www.gstatic.com/marketing-cms/assets/images/ec/00/5d847c1e4109ab4d2d82aec7726f/waze-logo.webp=s48-fcrop64=1,00000000ffffffff-rw"
        }
    ]


def get_places(type, zipcode):
    places_pool = _get_nearby_places(type, zipcode)
    places = []
    for _ in range(0, 3):
        description = None
        while description is None:
            place = random.choice(places_pool)
            places_pool.remove(place)
            description = _get_description(place)
        name = _get_name(place)
        photos = _get_photos(place)
        links = _get_links(place)
        place = Surprise(name, description, photos, links)
        places.append(place)
    return places