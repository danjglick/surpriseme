import random
import requests

URL = "https://musicbrainz.org/ws/2/release-group"
HEADERS = {
    "User-Agent": "SurpriseMe/1.0.0 ( danjglick@gmail.com )",
    "Accept": "application/json"
}


def get_albums(genre):
    params = {
        "query": f"tag:{genre} AND primarytype:album",
        "fmt": "json",
        "limit": 1 
    }
    response = requests.get(URL, params=params, headers=HEADERS)
    data = response.json()
    total = data["count"]
    offset = random.randint(0, min(total - 1, 9999)) # MusicBrainz practical cap ~10k
    params["offset"] = offset
    params["limit"] = 3
    response = requests.get(URL, params=params, headers=HEADERS)
    albums_pool = response.json()["release-groups"]
    albums = []
    for i in range(0, 3):
        albums.append(albums_pool[i]["title"])   
    return albums