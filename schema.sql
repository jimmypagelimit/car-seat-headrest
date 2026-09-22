PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS band (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    source_url TEXT,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS member (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    role TEXT,
    active_from INTEGER,
    active_to INTEGER,
    source_url TEXT
);

CREATE TABLE IF NOT EXISTS album (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL UNIQUE,
    release_year INTEGER,
    album_type TEXT,
    source_url TEXT
);

CREATE TABLE IF NOT EXISTS song (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    album_id INTEGER REFERENCES album(id) ON DELETE CASCADE,
    track_number INTEGER,
    source_url TEXT,
    UNIQUE(title, album_id)
);

CREATE TABLE IF NOT EXISTS source (
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL UNIQUE,
    title TEXT,
    fetched_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_song_album ON song(album_id);
