import random

from google_api_utilities import (
    RADIUS_METERS,
    get_coordinates,
    search_nearby
)


def get_parks(zipcode):
    coordinates = get_coordinates(zipcode)
    parks_pool = search_nearby(lat=coordinates[0], lng=coordinates[1], types=["park"], radius=RADIUS_METERS)
    parks = []
    for _ in range(0, 3):
        parks.append(random.choice(parks_pool)["displayName"]["text"])
    return parks
