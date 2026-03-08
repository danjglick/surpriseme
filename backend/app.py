from flask import Flask, jsonify, request, send_from_directory

from backend.get_walk import get_walk
from backend.get_places import get_places
from backend.get_movies import get_movies
from backend.get_albums import get_albums
from backend.surprise import Surprise

app = Flask(__name__, static_folder="../frontend", static_url_path="")


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/walk", methods=["GET"])
def fetch_walk():
    lat, lng = request.args.get("lat"), request.args.get("lng")
    walk: list[Surprise] = get_walk(lat, lng)
    return jsonify({ "message": walk })


@app.route("/api/bars", methods=["GET"])
def fetch_bars():
    zipcode = request.args.get("zipcode")
    bars: list[Surprise] = get_places("bar", zipcode)
    return jsonify({ "message": bars })


@app.route("/api/restaurants", methods=["GET"])
def fetch_restaurants():
    zipcode = request.args.get("zipcode")
    restaurants: list[Surprise] = get_places("restaurant", zipcode)
    return jsonify({ "message": restaurants })


@app.route("/api/parks", methods=["GET"])
def fetch_parks():
    zipcode = request.args.get("zipcode")
    parks: list[Surprise] = get_places("park", zipcode)
    return jsonify({ "message": parks })


@app.route("/api/galleries", methods=["GET"])
def fetch_galleries():
    zipcode = request.args.get("zipcode")
    galleries: list[Surprise] = get_places("art_gallery", zipcode)
    return jsonify({ "message": galleries })


@app.route("/api/bakeries", methods=["GET"])
def fetch_bakeries():
    zipcode = request.args.get("zipcode")
    bakeries: list[Surprise] = get_places("bakery", zipcode)
    return jsonify({ "message": bakeries })


@app.route("/api/bookstores", methods=["GET"])
def fetch_bookstores():
    zipcode = request.args.get("zipcode")
    bookstores: list[Surprise] = get_places("book_store", zipcode)
    return jsonify({ "message": bookstores })


@app.route("/api/campgrounds", methods=["GET"])
def fetch_campgrounds():
    zipcode = request.args.get("zipcode")
    campgrounds: list[Surprise] = get_places("campground", zipcode)
    return jsonify({ "message": campgrounds })


@app.route("/api/museums", methods=["GET"])
def fetch_museums():
    zipcode = request.args.get("zipcode")
    museums: list[Surprise] = get_places("museum", zipcode)
    return jsonify({ "message": museums })


@app.route("/api/nightclubs", methods=["GET"])
def fetch_nightclubs():
    zipcode = request.args.get("zipcode")
    nightclubs: list[Surprise] = get_places("night_club", zipcode)
    return jsonify({ "message": nightclubs })


@app.route("/api/theaters", methods=["GET"])
def fetch_theaters():
    zipcode = request.args.get("zipcode")
    theaters: list[Surprise] = get_places("movie_theater", zipcode)
    return jsonify({ "message": theaters })


@app.route("/api/cafes", methods=["GET"])
def fetch_cafes():
    zipcode = request.args.get("zipcode")
    cafes: list[Surprise] = get_places("cafe", zipcode)
    return jsonify({ "message": cafes })


@app.route("/api/attractions", methods=["GET"])
def fetch_attractions():
    zipcode = request.args.get("zipcode")
    attractions: list[Surprise] = get_places("tourist_attraction", zipcode)
    return jsonify({ "message": attractions })


@app.route("/api/amusement_parks", methods=["GET"])
def fetch_amusement_parks():
    zipcode = request.args.get("zipcode")
    amusement_parks: list[Surprise] = get_places("amusement_park", zipcode)
    return jsonify({ "message": amusement_parks })


@app.route("/api/bowling_alleys", methods=["GET"])
def fetch_bowling_alleys():
    zipcode = request.args.get("zipcode")
    bowling_alleys: list[Surprise] = get_places("bowling_alley", zipcode)
    return jsonify({ "message": bowling_alleys })


@app.route("/api/movies", methods=["GET"])
def fetch_movies():
    movies: list[Surprise] = get_movies()
    return jsonify({ "message": movies })
    

@app.route("/api/albums", methods=["GET"])
def fetch_albums():
    album_genre = request.args.get("album_genre")
    albums: list[Surprise] = get_albums(album_genre)
    return jsonify({ "message": albums })