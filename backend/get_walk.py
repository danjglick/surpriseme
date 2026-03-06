import os
import math
import random

from dotenv import load_dotenv; load_dotenv()
from global_land_mask import globe

from backend.surprise import Surprise

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
URL = "https://places.googleapis.com/v1/places:searchNearby"
FIELD_MASK = "places.googleMapsLinks"
HEADERS = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": GOOGLE_API_KEY,
    "X-Goog-FieldMask": FIELD_MASK
}
RADIUS_METERS = 1000
GOOGLE_ICON = "https://www.gstatic.com/marketing-cms/assets/images/0f/9a/58f1d92b46069b4a8bdc556b612c/google-maps.webp=s48-fcrop64=1,00000000ffffffff-rw"
MAX_ATTEMPTS = 100


def _random_nearby(lat, lng):
    for _ in range(MAX_ATTEMPTS):
        radius_deg = RADIUS_METERS / 111000  # approx conversion
        theta = random.random() * 2 * math.pi
        new_lat = lat + radius_deg * math.cos(theta)
        new_lng = lng + (radius_deg * math.sin(theta) / math.cos(math.radians(lat)))
        if globe.is_land(new_lat, new_lng):
            return new_lat, new_lng


def get_walk(lat, lng):
    coords = _random_nearby(float(lat), float(lng))
    link = {
        "href": f"https://www.google.com/maps/dir/?api=1&destination={coords[0]},{coords[1]}",
        "src": GOOGLE_ICON
    }
    walk = Surprise(name="", description="", photos=[], links=[link])
    return [walk]