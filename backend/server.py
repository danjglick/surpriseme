import os

from get_venues import get_venues

from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv; load_dotenv()

app = Flask(__name__, static_folder="../frontend", static_url_path="")


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/venue", methods=["GET"])
def api():
    try:
        zipcode = request.args.get("zipcode")
        print(f"Zipcode: {zipcode}")
        venues = get_venues()
        print(f"Venues: {venues}")
        return jsonify({"message": venues})
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)