-- SQLite schema and starter data for Car Seat Headrest.
-- The database.py script applies this structure and creates the database file.

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
