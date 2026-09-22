#!/usr/bin/env python3
"""Tiny SQLite-backed web app; no third-party dependencies required."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse
import html
import sqlite3

ROOT = Path(__file__).resolve().parent
DB = ROOT / "data" / "car-seat-headrest.sqlite3"


def query(sql, args=()):
    with sqlite3.connect(DB) as db:
        db.row_factory = sqlite3.Row
        return db.execute(sql, args).fetchall()


def page():
    albums = query("SELECT title, release_year, album_type, source_url FROM album ORDER BY release_year DESC, title")
    members = query("SELECT name, role, active_from, active_to FROM member ORDER BY active_from, name")
    songs = query("SELECT song.title, album.title AS album FROM song JOIN album ON album.id = song.album_id ORDER BY album.release_year DESC, song.track_number")
    def esc(value): return html.escape(str(value or ""))
    album_html = "".join(f'<article><h3>{esc(a["title"])}</h3><p>{esc(a["release_year"])} · {esc(a["album_type"])}</p><a href="{esc(a["source_url"])}">来源</a></article>' for a in albums)
    member_html = "".join(f'<li><strong>{esc(m["name"])}</strong> — {esc(m["role"])} ({esc(m["active_from"])}–{esc(m["active_to"]) or "至今"})</li>' for m in members)
    song_html = "".join(f'<li>{esc(s["title"])} <small>（{esc(s["album"])}）</small></li>' for s in songs) or '<li>运行 scrape.py 后可导入曲目数据。</li>'
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Car Seat Headrest · 资料库</title><link rel="stylesheet" href="/style.css"></head><body><main><header><p class="eyebrow">FAN ARCHIVE / SQLITE</p><h1>Car Seat Headrest</h1><p>一个关于 Car Seat Headrest 一切的一切的乐队资料库。</p></header><section><h2>专辑</h2><div class="grid">{album_html}</div></section><section><h2>成员</h2><ul>{member_html}</ul></section><section><h2>歌曲</h2><ul>{song_html}</ul></section><footer>数据来源：MusicBrainz 与各条目来源链接。仅供学习与粉丝资料整理。</footer></main></body></html>'''


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            body, content_type = page(), "text/html; charset=utf-8"
        elif path == "/style.css":
            body, content_type = (ROOT / "static" / "style.css").read_text(), "text/css; charset=utf-8"
        else:
            self.send_error(404); return
        data = body.encode("utf-8")
        self.send_response(200); self.send_header("Content-Type", content_type); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)


if __name__ == "__main__":
    if not DB.exists():
        import subprocess; subprocess.run(["python3", str(ROOT / "database.py")], check=True)
    print("Open http://localhost:8000")
    HTTPServer(("localhost", 8000), Handler).serve_forever()
