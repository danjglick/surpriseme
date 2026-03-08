import os
import random

import requests

from backend.surprise import Surprise
from backend.constants import (
	TMDB_API_KEY,
	TMDB_DISCOVER_URL,
	TMDB_PAGES_CAP
)

COMEDY_GENRE_ID = 35


def get_movies() -> list[Surprise]:
	params = {
		"api_key": TMDB_API_KEY,
		"language": "en-US",
		"page": 1
	}
	response = requests.get(TMDB_DISCOVER_URL, params=params).json()
	total_pages = min(response["total_pages"], TMDB_PAGES_CAP)
	random_page = random.randint(1, total_pages)
	params["page"] = random_page
	response = requests.get(TMDB_DISCOVER_URL, params=params)
	movies_pool = response.json()["results"]
	movies = []
	for _ in range(0, 3):
		movie = random.choice(movies_pool)
		name = movie["title"]
		year = movie["release_date"][0:4]
		name += f" - {year}"
		description = movie["overview"]
		photos = [f"https://image.tmdb.org/t/p/w500/{movie["backdrop_path"]}"]
		links = [""]
		movie = Surprise(name, description, photos, links)
		movies.append(movie)
	return movies