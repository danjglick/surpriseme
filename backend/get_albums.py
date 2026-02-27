import random
import requests

MUSICBRAINZ_URL = "https://musicbrainz.org/ws/2/release-group"
HEADERS = {
    "User-Agent": "SurpriseMe/1.0.0 ( danjglick@gmail.com )",
    "Accept": "application/json"
}
ROUGH_REQUESTS_LIMIT = 10000


def get_albums(genre):
    params = {
        "query": f"primarytype:album",
        "fmt": "json",
        "limit": 1 
    }
    response = requests.get(MUSICBRAINZ_URL, params=params, headers=HEADERS)
    data = response.json()
    total = data.get("count", 0)
    offset = random.randint(0, min(total - 1, ROUGH_REQUESTS_LIMIT))
    params["offset"] = offset
    params["limit"] = 3
    response = requests.get(MUSICBRAINZ_URL, params=params, headers=HEADERS)
    albums_pool = response.json()["release-groups"]
    albums = []
    for i in range(0, 3):
        album = albums_pool[i]
        album = {
            "name": album["title"],
            "disambiguator": f"({album["artist-credit"][0]["name"]})",
            "description": "This is an album description."
        }
        albums.append(album)
    return albums