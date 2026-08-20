import sqlite3
from datetime import datetime

DB_NAME = "dhanvantri.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_checkin_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            sleep_hours REAL,
            energy INTEGER,
            mood INTEGER,
            stress INTEGER,
            hydration INTEGER,
            activity_minutes INTEGER,
            notes TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def save_checkin(user_id, data):
    create_checkin_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO checkins (
            user_id,
            sleep_hours,
            energy,
            mood,
            stress,
            hydration,
            activity_minutes,
            notes,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        data.get("sleep_hours"),
        data.get("energy"),
        data.get("mood"),
        data.get("stress"),
        data.get("hydration"),
        data.get("activity_minutes"),
        data.get("notes"),
        datetime.now().isoformat(timespec="seconds")
    ))

    conn.commit()
    conn.close()


def get_recent_checkins(user_id, limit=7):
    create_checkin_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM checkins
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (user_id, limit))

    checkins = cursor.fetchall()

    conn.close()

    return [dict(row) for row in checkins]