import sqlite3
from datetime import datetime

DB_NAME = "dhanvantri.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_profile_table():
    """
    Creates the profiles table if it does not already exist.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,

            age INTEGER,
            gender TEXT,

            wellness_goal TEXT,
            activity_level TEXT,
            sleep_hours REAL,

            dietary_preference TEXT,
            wellness_interest TEXT,

            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,

            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def get_profile(user_id):
    """
    Returns the user's health/wellness profile.
    """

    create_profile_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM profiles
        WHERE user_id = ?
    """, (user_id,))

    profile = cursor.fetchone()

    conn.close()

    if profile:
        return dict(profile)

    return None


def save_profile(user_id, data):
    """
    Creates or updates a user's wellness profile.
    """

    create_profile_table()

    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now().isoformat(timespec="seconds")

    existing_profile = get_profile(user_id)

    if existing_profile:

        cursor.execute("""
            UPDATE profiles
            SET
                age = ?,
                gender = ?,
                wellness_goal = ?,
                activity_level = ?,
                sleep_hours = ?,
                dietary_preference = ?,
                wellness_interest = ?,
                updated_at = ?
            WHERE user_id = ?
        """, (
            data.get("age"),
            data.get("gender"),
            data.get("wellness_goal"),
            data.get("activity_level"),
            data.get("sleep_hours"),
            data.get("dietary_preference"),
            data.get("wellness_interest"),
            now,
            user_id
        ))

    else:

        cursor.execute("""
            INSERT INTO profiles (
                user_id,
                age,
                gender,
                wellness_goal,
                activity_level,
                sleep_hours,
                dietary_preference,
                wellness_interest,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            data.get("age"),
            data.get("gender"),
            data.get("wellness_goal"),
            data.get("activity_level"),
            data.get("sleep_hours"),
            data.get("dietary_preference"),
            data.get("wellness_interest"),
            now,
            now
        ))

    conn.commit()
    conn.close()


def delete_profile(user_id):
    """
    Deletes the user's wellness profile.
    """

    create_profile_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM profiles
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()