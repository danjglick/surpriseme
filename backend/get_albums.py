import random
import re

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

MUSICBRAINZ_URL = "https://musicbrainz.org/ws/2/release-group"
MUSICBRAINZ_HEADERS = {
    "User-Agent": "SurpriseMe/1.0.0 ( danjglick@gmail.com )",
    "Accept": "application/json"
}
MUSICBRAINZ_REQUESTS_CAP = 10000
WIKI_HEADERS = {
    "User-Agent": "AlbumReceptionFetcher/1.0 (danjglick@example.com)"
}


def _remove_templates(text: str) -> str:
    result = []
    depth = 0
    i = 0
    while i < len(text):
        if text[i:i+2] == '{{':
            depth += 1
            i += 2
        elif text[i:i+2] == '}}':
            depth = max(0, depth - 1)
            i += 2
        elif depth == 0:
            result.append(text[i])
            i += 1
        else:
            i += 1
    return ''.join(result)


def _remove_tables(text: str) -> str:
    result = []
    depth = 0
    i = 0
    while i < len(text):
        if text[i:i+2] == '{|':
            depth += 1
            i += 2
        elif text[i:i+2] == '|}':
            depth = max(0, depth - 1)
            i += 2
        elif depth == 0:
            result.append(text[i])
            i += 1
        else:
            i += 1
    return ''.join(result)


def _split_sentences(text: str) -> list[str]:
    ABBREVS = re.compile(
        r'\b(Mr|Mrs|Ms|Dr|Prof|Sr|Jr|St|Vol|vs|etc|approx|dept|est|govt|corp|inc|ltd|op|ed|trans)\.$',
        re.IGNORECASE
    )

    def split_non_abbrev(chunk: str) -> list[str]:
        parts = re.split(r'(?<=\.)\s+(?=[A-Z])', chunk)
        merged = []
        buffer = ''
        for part in parts:
            if buffer:
                if ABBREVS.search(buffer):
                    buffer = buffer + ' ' + part
                else:
                    merged.append(buffer)
                    buffer = part
            else:
                buffer = part
        if buffer:
            merged.append(buffer)
        return merged

    parts = re.split(r'(\."|\?"|!")', text)
    joined = []
    i = 0
    while i < len(parts):
        if i + 1 < len(parts) and parts[i + 1] in ('."', '?"', '!"'):
            joined.append(parts[i] + parts[i + 1])
            i += 2
        else:
            joined.append(parts[i])
            i += 1
    result = []
    for chunk in joined:
        result.extend(split_non_abbrev(chunk))
    return [s.strip() for s in result if s.strip()]


def _get_reception(album_name: str, artist: str) -> str | None:
    search_url = "https://en.wikipedia.org/w/api.php"
    try:
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": f"{album_name} {artist} album",
            "format": "json",
            "srlimit": 5
        }
        response = requests.get(search_url, params=search_params, headers=WIKI_HEADERS, timeout=5)
        response.raise_for_status()
        results = response.json().get("query", {}).get("search", [])
        if not results:
            return None
        page_title = results[0]["title"]
        sections_params = {
            "action": "parse",
            "page": page_title,
            "prop": "sections",
            "format": "json"
        }
        response = requests.get(search_url, params=sections_params, headers=WIKI_HEADERS, timeout=5)
        response.raise_for_status()
        sections = response.json().get("parse", {}).get("sections", [])
        reception_section = None
        for section in sections:
            if section["line"].lower() == "critical reception":
                reception_section = section
                break
        if not reception_section:
            for section in sections:
                if "reception" in section["line"].lower():
                    reception_section = section
                    break
        if not reception_section:
            return None
        content_params = {
            "action": "parse",
            "page": page_title,
            "prop": "wikitext",
            "section": reception_section["index"],
            "format": "json"
        }
        response = requests.get(search_url, params=content_params, headers=WIKI_HEADERS, timeout=5)
        response.raise_for_status()
        wikitext = response.json().get("parse", {}).get("wikitext", {}).get("*", "")
        cleaned = _remove_templates(wikitext)
        cleaned = _remove_tables(cleaned)
        cleaned = re.sub(r'<!--.*?-->', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', cleaned)
        cleaned = re.sub(r'<ref[^>]*/>', '', cleaned)
        cleaned = re.sub(r'<ref[^>]*>[^<]*</ref>', '', cleaned)
        cleaned = re.sub(r'<[^>]+>', '', cleaned)
        cleaned = re.sub(r'={2,}.*?={2,}', '', cleaned)
        cleaned = re.sub(r"'{2,}", '', cleaned)
        cleaned = re.sub(r'(\[\d+\])+', ' ', cleaned)
        cleaned = cleaned.replace('\u201c', '"').replace('\u201d', '"')
        cleaned = cleaned.replace('\u2018', "'").replace('\u2019', "'")
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned).strip()
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned).strip()
        cleaned = re.sub(r'\.{2,}', '…', cleaned)  
        sentences = _split_sentences(cleaned)
        skip_terms = re.compile(r'\bcharts?\b|\bstars?\b', re.IGNORECASE)
        def is_disqualified(sentence: str) -> bool:
            if skip_terms.search(sentence):
                return True
            for num in re.findall(r'\b(\d+)\b', sentence):
                if re.match(r'^(19|20)\d{2}$', num):
                    continue
                if not re.search(rf'\b{re.escape(num)}\b', album_name + ' ' + artist, re.IGNORECASE):
                    return True
            return False
        selected = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            if not is_disqualified(sentence):
                selected.append(sentence)
            if len(selected) == 3:
                break
        return ' '.join(selected) if selected else None
    except Exception:
        return None


def get_albums(genre):
    params = {
        "query": "primarytype:album",
        "fmt": "json",
        "limit": 1
    }
    response = requests.get(MUSICBRAINZ_URL, params=params, headers=MUSICBRAINZ_HEADERS)
    data = response.json()
    total = data.get("count", 0)
    albums = []
    attempts = 0
    max_attempts = 20
    while len(albums) < 3 and attempts < max_attempts:
        offset = random.randint(0, min(total - 1, MUSICBRAINZ_REQUESTS_CAP))
        params["offset"] = offset
        params["limit"] = 20
        response = requests.get(MUSICBRAINZ_URL, params=params, headers=MUSICBRAINZ_HEADERS)
        pool = response.json().get("release-groups", [])
        # Fetch receptions in parallel
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(
                    _get_reception,
                    album["title"],
                    album['artist-credit'][0]['name']
                ): album
                for album in pool
            }
            for future in as_completed(futures):
                if len(albums) >= 3:
                    break
                album = futures[future]
                reception = future.result()
                if reception:
                    albums.append({
                        "name": album["title"],
                        "disambiguator": f"({album['artist-credit'][0]['name']})",
                        "description": reception
                    })
        attempts += 1
    return albums