#!/usr/bin/env python3
"""Fetch public MusicBrainz release-group data into the local SQLite database.

MusicBrainz asks clients to identify themselves and to avoid excessive request
rates. This importer makes one request and records the source URL for review.
Run: python3 scrape.py
"""
from pathlib import Path
import json
import sqlite3
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "car-seat-headrest.sqlite3"
API = "https://musicbrainz.org/ws/2/artist/?query=artist:%22Car%20Seat%20Headrest%22&fmt=json"
USER_AGENT = "car-seat-headrest-fan-site/1.0 (https://github.com/jimmypagelimit/car-seat-headrest)"


def get_json(url):
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(request, timeout=20) as response:
        return json.load(response)


def main():
    ROOT.joinpath("data").mkdir(exist_ok=True)
    if not DB_PATH.exists():
        import subprocess
        subprocess.run(["python3", str(ROOT / "database.py")], check=True)

    artists = get_json(API).get("artists", [])
    artist = next((item for item in artists if item.get("name", "").lower() == "car seat headrest"), None)
    if not artist:
        raise RuntimeError("Car Seat Headrest was not found in MusicBrainz")

    release_url = f"https://musicbrainz.org/ws/2/release-group/?artist={artist['id']}&type=album&limit=100&fmt=json"
    release_groups = get_json(release_url).get("release-groups", [])
    with sqlite3.connect(DB_PATH) as db:
        db.execute("INSERT OR IGNORE INTO source(url, title) VALUES (?, ?)", (API, "MusicBrainz artist search"))
        db.execute("INSERT OR IGNORE INTO source(url, title) VALUES (?, ?)", (release_url, "MusicBrainz album release groups"))
        for item in release_groups:
            date = item.get("first-release-date", "")
            year = int(date[:4]) if date[:4].isdigit() else None
            db.execute(
                "INSERT OR IGNORE INTO album(title, release_year, album_type, source_url) VALUES (?, ?, ?, ?)",
                (item["title"], year, "录音室专辑", f"https://musicbrainz.org/release-group/{item['id']}"),
            )
        db.commit()
    print(f"Imported {len(release_groups)} album release groups from MusicBrainz.")
    time.sleep(1)


if __name__ == "__main__":
    main()
