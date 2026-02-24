import random

from google_api_utilities import (
    RADIUS_METERS, 
    get_coordinates, 
    search_nearby
)


def get_bars(zipcode):
    coordinates = get_coordinates(zipcode)
    bars_pool = search_nearby(lat=coordinates[0], lng=coordinates[1], types=["bar"], radius=RADIUS_METERS)
    bars = []
    for _ in range(0, 3):
        bars.append(random.choice(bars_pool)["displayName"]["text"])
    return bars