import random
import requests

BASE_URL = "https://musicbrainz.org/ws/2/release-group"
HEADERS = {
    "User-Agent": "SurpriseMe/1.0.0 ( danjglick@gmail.com )",
    "Accpet": "application/json"
}


def get_albums(genre):
    params = {
        "query": f"tag:{genre} AND primarytype:album",
        "fmt": "json",
        "limit": 1 
    }
    response = requests.get(BASE_URL, params=params, headers=HEADERS)
    data = response.json()
    total = data["count"]
    offset = random.randint(0, min(total - 1, 9999)) # MusicBrainz practical cap ~10k
    params["offset"] = offset
    params["limit"] = 1
    response = requests.get(BASE_URL, params=params, headers=HEADERS)
    album = response.json()["release-groups"][0]
    return {
        "title": album["title"],
        "artist": album["artist-credit"][0]["name"],
        "mbid": album["id"]
    }
