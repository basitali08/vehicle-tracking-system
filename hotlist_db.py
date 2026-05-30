"""
Hotlist database for managing suspected vehicle plates.
Uses SQLite for simplicity.
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = 'hotlist.db'


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS hotlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate TEXT NOT NULL UNIQUE,
            reason TEXT DEFAULT '',
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate TEXT NOT NULL,
            image_name TEXT,
            latitude REAL DEFAULT 0.0,
            longitude REAL DEFAULT 0.0,
            location_name TEXT DEFAULT 'Unknown',
            detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()


def add_to_hotlist(plate, reason=''):
    conn = get_connection()
    try:
        conn.execute("INSERT OR IGNORE INTO hotlist (plate, reason) VALUES (?, ?)", (plate, reason))
        conn.commit()
    finally:
        conn.close()


def remove_from_hotlist(plate):
    conn = get_connection()
    conn.execute("DELETE FROM hotlist WHERE plate = ?", (plate,))
    conn.commit()
    conn.close()


def get_hotlist():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM hotlist ORDER BY added_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def is_hotlisted(plate):
    conn = get_connection()
    row = conn.execute("SELECT 1 FROM hotlist WHERE plate = ?", (plate,)).fetchone()
    conn.close()
    return row is not None


def log_detection(plate, image_name='', lat=0.0, lng=0.0, location='Unknown'):
    conn = get_connection()
    conn.execute(
        "INSERT INTO detections (plate, image_name, latitude, longitude, location_name) VALUES (?, ?, ?, ?, ?)",
        (plate, image_name, lat, lng, location)
    )
    conn.commit()
    conn.close()


def get_detection_history(plate=None, limit=50):
    conn = get_connection()
    if plate:
        rows = conn.execute(
            "SELECT * FROM detections WHERE plate = ? ORDER BY detected_at DESC LIMIT ?",
            (plate, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM detections ORDER BY detected_at DESC LIMIT ?", (limit,)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_alert_count():
    conn = get_connection()
    row = conn.execute("""
        SELECT COUNT(*) as count FROM detections d
        INNER JOIN hotlist h ON d.plate = h.plate
    """).fetchone()
    conn.close()
    return row['count']


def seed_from_file(filepath='samples/hotlist_plates.txt'):
    if os.path.exists(filepath):
        with open(filepath) as f:
            for line in f:
                plate = line.strip()
                if plate:
                    add_to_hotlist(plate, 'Suspicious vehicle')


if __name__ == '__main__':
    init_db()
    seed_from_file()
    print(f"Hotlist contains {len(get_hotlist())} plates")
    for h in get_hotlist()[:5]:
        print(f"  {h['plate']} - {h['reason']}")
