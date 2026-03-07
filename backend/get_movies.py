import os
import random

import requests

from backend.surprise import Surprise

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
TMDB_URL = "https://api.themoviedb.org/3/discover/movie"
CONFIG_URL = "https://api.themoviedb.org/3/configuration"


def _lookup_genre_id(movie_genre):
	match str.lower(movie_genre):
		case "action":
			return 28
		case "adventure":
			return 12
		case "animation" | "cartoon":
			return 16
		case "comedy":
			return 35
		case "crime":
			return 80
		case "documentary" | "doc":
			return 90
		case "drama":
			return 18
		case "family" | "kids":
			return 10751
		case "fantasy":
			return 14
		case "history":
			return 36
		case "horror":
			return 27
		case "musical":
			return 10402
		case "mystery":
			return 9648
		case "romance" | "romcom" | "rom com" | "rom-com":
			return 10749
		case "science fiction" | "scifi" | "sci fi" | "sci-fi":
			return 878
		case "thriller":
			return 53
		case "war":
			return 10752
		case "western":
			return 37


def _get_photo():
	return


def get_movies(movie_genre):
	genre_id = _lookup_genre_id(movie_genre)
	params = {
		"api_key": TMDB_API_KEY,
		"with_genres": genre_id,
		"language": "en-US",
		"page": 1
	}
	response = requests.get(TMDB_URL, params=params).json()
	total_pages = min(response["total_pages"], 450) # TMDB limits page queries to 500
	random_page = random.randint(1, total_pages)
	params["page"] = random_page
	response = requests.get(TMDB_URL, params=params)
	movies_pool = response.json()["results"]
	movies = []
	for _ in range(0, 3):
		movie = random.choice(movies_pool)
		name = movie["title"]
		year = movie["release_date"][0:4]
		name += f" - {year}"
		description = movie["overview"]
		photo = f"https://image.tmdb.org/t/p/w500/{movie["backdrop_path"]}"
		links = [""]
		movie = Surprise(name, description, photo, links)
		movies.append(movie)
	return movies