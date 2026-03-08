import random

import requests

from backend.surprise import Surprise
from backend.constants import( 
    GOOGLE_API_KEY, 
    GOOGLE_SEARCHTEXT_URL, 
    GOOGLE_ICON,
    WAZE_ICON
)

FIELD_MASK = "places.displayName,places.googleMapsLinks,places.addressComponents,places.editorialSummary,places.reviewSummary,places.photos,nextPageToken"
HEADERS = { 
    "Content-Type": "application/json", 
    "X-Goog-Api-Key": GOOGLE_API_KEY, 
    "X-Goog-FieldMask": FIELD_MASK 
}


def _get_nearby_places(type: str, zipcode: str) -> list[dict]:
    body = {
        "textQuery": f"{type} near {zipcode}",
        "minRating": "4.0"
    }
    response = requests.post(GOOGLE_SEARCHTEXT_URL, headers=HEADERS, json=body)
    data = response.json()
    places = data["places"]
    while "nextPageToken" in data:
        body["pageToken"] = data["nextPageToken"]
        response = requests.post(GOOGLE_SEARCHTEXT_URL, headers=HEADERS, json=body)
        data = response.json()
        for place in data["places"]: 
            places.append(place)
    return places


def _get_name(place: dict) -> str:
    name = place["displayName"]["text"]
    locale = None
    for component in place["addressComponents"]:
        if "neighborhood" in component["types"]: 
            locale = component["longText"]
        elif "locality" in component["types"]: 
            locale = component["longText"]
    name += f" - {locale}"
    return name


def _get_description(place: dict) -> str:
    description = None
    if "reviewSummary" in place:
        description = place["reviewSummary"]["text"]["text"]
        description = " ".join(line.strip() for line in description.splitlines())
    elif "editorialSummary" in place:
        description = place["editorialSummary"]["text"]
    return description


def _get_photos(place: dict) -> list[str]:
    photos = []
    for i in range(0, len(place["photos"])):
        photo_name = place["photos"][i]["name"]
        photos_url = f"https://places.googleapis.com/v1/{photo_name}/media?maxWidthPx=400&skipHttpRedirect=true&key={GOOGLE_API_KEY}"
        response = requests.get(photos_url)
        data = response.json()
        photo = data.get("photoUri")
        photos.append(photo)
    return photos


def _get_links(place: dict) -> list[dict]:
    return [
        { 
            "href": place["googleMapsLinks"]["placeUri"],
            "src": GOOGLE_ICON
        },
        {
            "href": "",
            "src": WAZE_ICON
        }
    ]


def get_places(type: str, zipcode: str) -> list[Surprise]:
    nearby_places = _get_nearby_places(type, zipcode)
    places = []
    for _ in range(0, 3):
        description = None
        while description is None:
            place = random.choice(nearby_places)
            nearby_places.remove(place)
            description = _get_description(place)
        name = _get_name(place)
        photos = _get_photos(place)
        links = _get_links(place)
        place = Surprise(name, description, photos, links)
        places.append(place)
    return places