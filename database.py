#!/usr/bin/env python3
"""Initialize the Car Seat Headrest SQLite database with starter data."""
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "car-seat-headrest.sqlite3"

DATA_DIR.mkdir(parents=True, exist_ok=True)

with sqlite3.connect(DB_PATH) as connection:
    connection.executescript(
        """
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS band (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS member (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            role TEXT,
            active_from INTEGER,
            active_to INTEGER
        );

        CREATE TABLE IF NOT EXISTS album (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL UNIQUE,
            release_year INTEGER,
            album_type TEXT
        );

        CREATE TABLE IF NOT EXISTS song (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            album_id INTEGER REFERENCES album(id),
            track_number INTEGER,
            UNIQUE(title, album_id)
        );

        INSERT OR IGNORE INTO band (id, name, description)
        VALUES (1, 'Car Seat Headrest',
                '一个关于 Car Seat Headrest 一切的一切的乐队资料库。');

        INSERT OR IGNORE INTO member (name, role, active_from)
        VALUES ('Will Toledo', '主唱、吉他、词曲创作', 2010);

        INSERT OR IGNORE INTO album (title, release_year, album_type)
        VALUES
            ('Twin Fantasy', 2018, '录音室专辑'),
            ('Teens of Denial', 2016, '录音室专辑');

        INSERT OR IGNORE INTO song (title, album_id, track_number)
        SELECT 'My Boy (Twin Fantasy)', id, 1 FROM album WHERE title = 'Twin Fantasy';
        """
    )

print(f"SQLite database initialized at {DB_PATH}")
