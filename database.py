#!/usr/bin/env python3
"""Create the SQLite database and load a small, useful starter dataset."""
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "car-seat-headrest.sqlite3"

SCHEMA = (ROOT / "schema.sql").read_text(encoding="utf-8")
DATA_DIR.mkdir(parents=True, exist_ok=True)

with sqlite3.connect(DB_PATH) as connection:
    connection.executescript(SCHEMA)
    connection.execute("""
        INSERT OR IGNORE INTO band (id, name, description)
        VALUES (1, 'Car Seat Headrest',
                '一个关于 Car Seat Headrest 一切的一切的乐队资料库。')
    """)
    connection.executemany(
        "INSERT OR IGNORE INTO member (name, role, active_from) VALUES (?, ?, ?)",
        [
            ("Will Toledo", "主唱、吉他、词曲创作", 2010),
            ("Ethan Ives", "吉他、贝斯", 2016),
            ("Jacob Bloom", "鼓", 2016),
            ("Andrew Katz", "鼓、打击乐", 2015),
        ],
    )
    connection.executemany(
        "INSERT OR IGNORE INTO album (title, release_year, album_type, source_url) VALUES (?, ?, ?, ?)",
        [
            ("Twin Fantasy", 2018, "录音室专辑", "https://en.wikipedia.org/wiki/Twin_Fantasy"),
            ("Teens of Denial", 2016, "录音室专辑", "https://en.wikipedia.org/wiki/Teens_of_Denial"),
            ("Making a Door Less Open", 2020, "录音室专辑", "https://en.wikipedia.org/wiki/Making_a_Door_Less_Open"),
        ],
    )

print(f"SQLite database initialized at {DB_PATH}")
