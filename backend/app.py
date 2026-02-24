import os

from get_places import get_places
from get_movies import get_movies
from get_albums import get_albums

from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv; load_dotenv()

app = Flask(__name__, static_folder="../frontend", static_url_path="")


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/bars", methods=["GET"])
def fetch_bars():
    zipcode = request.args.get("zipcode")
    bars = get_places("bar", zipcode)
    return jsonify({"message": f"{bars}"})


@app.route("/api/restaurants", methods=["GET"])
def fetch_restaurants():
    zipcode = request.args.get("zipcode")
    restaurants = get_places("restaurant", zipcode)
    return jsonify({"message": f"{restaurants}"})


@app.route("/api/parks", methods=["GET"])
def fetch_parks():
    zipcode = request.args.get("zipcode")
    parks = get_places("park", zipcode)
    return jsonify({"message": f"{parks}"})


@app.route("/api/galleries", methods=["GET"])
def fetch_galleries():
    zipcode = request.args.get("zipcode")
    galleries = get_places("art_gallery", zipcode)
    return jsonify({"message": f"{galleries}"})


@app.route("/api/bakeries", methods=["GET"])
def fetch_bakeries():
    zipcode = request.args.get("zipcode")
    bakeries = get_places("bakery", zipcode)
    return jsonify({"message": f"{bakeries}"})


@app.route("/api/bookstores", methods=["GET"])
def fetch_bookstores():
    zipcode = request.args.get("zipcode")
    bookstores = get_places("book_store", zipcode)
    return jsonify({"message": f"{bookstores}"})


@app.route("/api/campgrounds", methods=["GET"])
def fetch_campgrounds():
    zipcode = request.args.get("zipcode")
    campgrounds = get_places("campground", zipcode)
    return jsonify({"message": f"{campgrounds}"})


@app.route("/api/museums", methods=["GET"])
def fetch_museums():
    zipcode = request.args.get("zipcode")
    museums = get_places("museum", zipcode)
    return jsonify({"message": f"{museums}"})


@app.route("/api/nightclubs", methods=["GET"])
def fetch_nightclubs():
    zipcode = request.args.get("zipcode")
    nightclubs = get_places("night_club", zipcode)
    return jsonify({"message": f"{nightclubs}"})


@app.route("/api/theaters", methods=["GET"])
def fetch_theaters():
    zipcode = request.args.get("zipcode")
    theaters = get_places("movie_theater", zipcode)
    return jsonify({"message": f"{theaters}"})


@app.route("/api/cafes", methods=["GET"])
def fetch_cafes():
    zipcode = request.args.get("zipcode")
    cafes = get_places("cafe", zipcode)
    return jsonify({"message": f"{cafes}"})


@app.route("/api/attractions", methods=["GET"])
def fetch_attractions():
    zipcode = request.args.get("zipcode")
    attractions = get_places("tourist_attraction", zipcode)
    return jsonify({"message": f"{attractions}"})


@app.route("/api/amusement_parks", methods=["GET"])
def fetch_amusement_parks():
    zipcode = request.args.get("zipcode")
    amusement_parks = get_places("amusement_park", zipcode)
    return jsonify({"message": f"{amusement_parks}"})


@app.route("/api/bowling_alleys", methods=["GET"])
def fetch_bowling_alleys():
    zipcode = request.args.get("zipcode")
    bowling_alleys = get_places("bowling_alley", zipcode)
    return jsonify({"message": f"{bowling_alleys}"})


@app.route("/api/movies", methods=["GET"])
def fetch_movies():
    movie_genre = request.args.get("movie_genre")
    movies = get_movies(movie_genre)
    return jsonify({"message": f"{movies}"})
    

@app.route("/api/albums", methods=["GET"])
def fetch_albums():
    album_genre = request.args.get("album_genre")
    albums = get_albums(album_genre)
    return jsonify({"message": f"{albums}"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)