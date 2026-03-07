import math
import os
import random

from dotenv import load_dotenv; load_dotenv()
import requests

from backend.surprise import Surprise

LNG = -71.032229
LAT = 42.364661
RADIUS_METERS = 400
OSRM_URL = f"http://router.project-osrm.org/trip/v1/foot/{LNG},{LAT};radius=1000.0"
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
PLACES_URL = "https://places.googleapis.com/v1/places:searchNearby"
FIELD_MASK = "places.location"
PLACES_HEADERS = { 
    "Content-Type": "application/json", 
    "X-Goog-Api-Key": GOOGLE_API_KEY, 
    "X-Goog-FieldMask": FIELD_MASK 
}
GOOGLE_ICON = "https://www.gstatic.com/marketing-cms/assets/images/0f/9a/58f1d92b46069b4a8bdc556b612c/google-maps.webp=s48-fcrop64=1,00000000ffffffff-rw"


def _get_waypoints():
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
    response = requests.post(PLACES_URL, headers=PLACES_HEADERS, json=body)
    data = response.json()
    places = data["places"]
    waypoints = []
    for _ in range(0, 5):
        waypoint = random.choice(places)
        location = waypoint["location"]
        waypoints.append(location)
        places.remove(waypoint)
    return waypoints


def _sort_by_angle(waypoints, lat, lng):
    def angle(wp):
        return math.atan2(wp["longitude"] - lng, wp["latitude"] - lat)
    return sorted(waypoints, key=angle)


def get_walk(lat, lng):
    w = _get_waypoints()
    w = _sort_by_angle(w, LAT, LNG)
    lat1, lng1 = w[0]["latitude"], w[0]["longitude"]
    lat2, lng2 = w[1]["latitude"], w[1]["longitude"]
    lat3, lng3 = w[2]["latitude"], w[2]["longitude"]
    lat4, lng4 = w[3]["latitude"], w[3]["longitude"]
    lat5, lng5 = w[4]["latitude"], w[4]["longitude"]
    url = f"https://www.google.com/maps/dir/?api=1&origin={LAT},{LNG}&destination={LAT},{LNG}&waypoints={lat1},{lng1}|{lat2},{lng2}|{lat3},{lng3}|{lat4},{lng4}|{lat5},{lng5}&travelmode=walking"
    walk = Surprise(name="", description="", photos=[], links=[{ "href": url, "src": GOOGLE_ICON }])
    return [walk]


# http://router.project-osrm.org/trip/v1/foot/-71.032229,42.364661;radius=1000.0

# GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
# URL = "https://places.googleapis.com/v1/places:searchNearby"
# FIELD_MASK = "places.googleMapsLinks"
# HEADERS = {
#     "Content-Type": "application/json",
#     "X-Goog-Api-Key": GOOGLE_API_KEY,
#     "X-Goog-FieldMask": FIELD_MASK
# }
# RADIUS_METERS = 1000
# GOOGLE_ICON = "https://www.gstatic.com/marketing-cms/assets/images/0f/9a/58f1d92b46069b4a8bdc556b612c/google-maps.webp=s48-fcrop64=1,00000000ffffffff-rw"
# MAX_ATTEMPTS = 100


# def _random_nearby(lat, lng):
#     for _ in range(MAX_ATTEMPTS):
#         radius_deg = RADIUS_METERS / 111000  # approx conversion
#         theta = random.random() * 2 * math.pi
#         new_lat = lat + radius_deg * math.cos(theta)
#         new_lng = lng + (radius_deg * math.sin(theta) / math.cos(math.radians(lat)))
#         if globe.is_land(new_lat, new_lng):
#             return new_lat, new_lng


# def get_walk(lat, lng):
#     coords = _random_nearby(float(lat), float(lng))
#     link = {
#         "href": f"https://www.google.com/maps/dir/?api=1&destination={coords[0]},{coords[1]}",
#         "src": GOOGLE_ICON
#     }
#     walk = Surprise(name="", description="", photos=[], links=[link])
#     return [walk]