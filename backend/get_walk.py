import math
import random

import requests

from backend.surprise import Surprise
from backend.constants import(
    GOOGLE_API_KEY, 
    GOOGLE_SEARCHNEARBY_URL, 
    GOOGLE_ICON
)

FIELD_MASK = "places.location"
HEADERS = { 
    "Content-Type": "application/json", 
    "X-Goog-Api-Key": GOOGLE_API_KEY, 
    "X-Goog-FieldMask": FIELD_MASK 
}
RADIUS_METERS = 350
LNG = -71.032229
LAT = 42.364661


def _get_waypoints() -> list:
    body = {
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": LAT,
                    "longitude": LNG
                },
                "radius": RADIUS_METERS
            }
        }
    }
    response = requests.post(GOOGLE_SEARCHNEARBY_URL, headers=HEADERS, json=body)
    data = response.json()
    places = data["places"]
    waypoints = []
    for _ in range(0, 5):
        place = random.choice(places)
        waypoint = place["location"]
        waypoints.append(waypoint)
        places.remove(place)
    return waypoints


def _sort_by_angle(waypoints, lat, lng):
    def angle(wp):
        return math.atan2(wp["longitude"] - lng, wp["latitude"] - lat)
    return sorted(waypoints, key=angle)


def get_walk(lat, lng) -> list[Surprise]:
    w = _get_waypoints()
    w = _sort_by_angle(w, LAT, LNG)
    lat1, lng1 = w[0]["latitude"], w[0]["longitude"]
    lat2, lng2 = w[1]["latitude"], w[1]["longitude"]
    lat3, lng3 = w[2]["latitude"], w[2]["longitude"]
    lat4, lng4 = w[3]["latitude"], w[3]["longitude"]
    lat5, lng5 = w[4]["latitude"], w[4]["longitude"]
    href = f"https://www.google.com/maps/dir/?api=1&origin={LAT},{LNG}&destination={LAT},{LNG}&waypoints={lat1},{lng1}|{lat2},{lng2}|{lat3},{lng3}|{lat4},{lng4}|{lat5},{lng5}&travelmode=walking"
    walk = Surprise(name="", description="", photos=[], links=[{ "href": href, "src": GOOGLE_ICON }])
    return [walk]