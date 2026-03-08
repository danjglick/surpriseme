import os

from dotenv import load_dotenv; load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_SEARCHNEARBY_URL = "https://places.googleapis.com/v1/places:searchNearby"
GOOGLE_SEARCHTEXT_URL = "https://places.googleapis.com/v1/places:searchText"
GOOGLE_ICON = "https://www.gstatic.com/marketing-cms/assets/images/0f/9a/58f1d92b46069b4a8bdc556b612c/google-maps.webp=s48-fcrop64=1,00000000ffffffff-rw"

MUSICBRAINZ_URL = "https://musicbrainz.org/ws/2/release-group"
MUSICBRAINZ_HEADERS = {
    "User-Agent": "SurpriseMe/1.0.0 ( danjglick@gmail.com )",
    "Accept": "application/json"
}
MUSICBRAINZ_REQUESTS_CAP = 10000

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
TMDB_DISCOVER_URL = "https://api.themoviedb.org/3/discover/movie"
TMDB_PAGES_CAP = 500

WAZE_ICON = "https://www.gstatic.com/marketing-cms/assets/images/ec/00/5d847c1e4109ab4d2d82aec7726f/waze-logo.webp=s48-fcrop64=1,00000000ffffffff-rw"

WIKIPEDIA_URL = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_HEADERS = {
    "User-Agent": "AlbumReceptionFetcher/1.0 (danjglick@example.com)"
}