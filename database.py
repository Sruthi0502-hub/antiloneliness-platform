"""
Database Module for Sentimate
Handles SQLite database connections and all data operations.

Tables:
- users       : User accounts (id, username, password_hash, created_at)
- reminders   : Medication reminders (id, user_id, medicine_name, time, created_at)
- chat_history: Chat message log (id, user_id, sender, message, timestamp)
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

# ===== CONFIGURATION =====

DB_PATH = os.environ.get('DB_PATH', 'data/sentimate.db')


# ===== CONNECTION =====

def get_connection() -> sqlite3.Connection:
    """
    Create and return a new SQLite database connection.
    Row factory set so rows behave like dicts.
    """
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ===== INITIALIZATION =====

def init_db() -> None:
    """
    Create all required tables if they do not already exist.
    Safe to call on every application startup.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()

        # --- Users table ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT    NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT    NOT NULL,
                created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
            )
        """)

        # --- Reminders table ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                medicine_name TEXT    NOT NULL,
                time          TEXT    NOT NULL,
                created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
            )
        """)

        # --- Chat History table ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id   INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                sender    TEXT    NOT NULL CHECK(sender IN ('user', 'bot')),
                message   TEXT    NOT NULL,
                timestamp TEXT    NOT NULL DEFAULT (datetime('now'))
            )
        """)

        # --- User Preferences table ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                pref_key   TEXT    NOT NULL,
                pref_value TEXT    NOT NULL,
                updated_at TEXT    NOT NULL DEFAULT (datetime('now')),
                UNIQUE(user_id, pref_key)
            )
        """)

        conn.commit()
        print("Database initialized successfully.")
    finally:
        conn.close()




# ===== USER PREFERENCE FUNCTIONS =====

def save_user_preference(user_id: int, pref_key: str, pref_value: str) -> None:
    """
    Upsert a user preference key/value pair.
    Example: save_user_preference(1, 'language', 'tamil')
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO user_preferences (user_id, pref_key, pref_value, updated_at)
            VALUES (?, ?, ?, datetime('now'))
            ON CONFLICT(user_id, pref_key) DO UPDATE SET
                pref_value = excluded.pref_value,
                updated_at = excluded.updated_at
            """,
            (user_id, pref_key, pref_value)
        )
        conn.commit()
    finally:
        conn.close()


def get_user_preference(user_id: int, pref_key: str, default: str = None) -> Optional[str]:
    """
    Retrieve a single user preference value.
    Returns default if not found.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT pref_value FROM user_preferences WHERE user_id = ? AND pref_key = ?",
            (user_id, pref_key)
        )
        row = cursor.fetchone()
        return row['pref_value'] if row else default
    finally:
        conn.close()


# ===== USER FUNCTIONS =====

def create_user(username: str, password_hash: str) -> Dict[str, Any]:
    """
    Insert a new user into the database.

    Args:
        username: Unique username (case-insensitive)
        password_hash: Bcrypt / werkzeug hashed password

    Returns:
        Dict with new user's id and username

    Raises:
        ValueError: If username already exists
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username.strip(), password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return {'id': user_id, 'username': username}
    except sqlite3.IntegrityError:
        raise ValueError(f"Username '{username}' is already taken.")
    finally:
        conn.close()


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user record by username.

    Args:
        username: The username to look up

    Returns:
        User dict or None if not found
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, password_hash, created_at FROM users WHERE username = ? COLLATE NOCASE",
            (username.strip(),)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user record by primary key.

    Args:
        user_id: The user's integer ID

    Returns:
        User dict or None if not found
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, created_at FROM users WHERE id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


# ===== REMINDER FUNCTIONS =====

def add_reminder_db(user_id: int, medicine_name: str, time: str) -> Dict[str, Any]:
    """
    Insert a new medication reminder for a user.

    Args:
        user_id: Owner's user ID
        medicine_name: Name of the medication
        time: Reminder time in HH:MM format

    Returns:
        Dict with the new reminder's data
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reminders (user_id, medicine_name, time) VALUES (?, ?, ?)",
            (user_id, medicine_name.strip(), time.strip())
        )
        conn.commit()
        reminder_id = cursor.lastrowid
        return {
            'id': reminder_id,
            'user_id': user_id,
            'medicine_name': medicine_name,
            'time': time
        }
    finally:
        conn.close()


def get_reminders_for_user(user_id: int) -> List[Dict[str, Any]]:
    """
    Retrieve all reminders for a given user, sorted by time.

    Args:
        user_id: The user's ID

    Returns:
        List of reminder dicts
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, user_id, medicine_name, time, created_at FROM reminders WHERE user_id = ? ORDER BY time ASC",
            (user_id,)
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def delete_reminder_db(reminder_id: int, user_id: int) -> bool:
    """
    Delete a reminder belonging to the given user.

    Args:
        reminder_id: ID of the reminder to delete
        user_id: Must match the reminder's owner (security check)

    Returns:
        True if deleted, False if not found / not owned by user
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM reminders WHERE id = ? AND user_id = ?",
            (reminder_id, user_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


# ===== CHAT HISTORY FUNCTIONS =====

def save_message(user_id: int, sender: str, message: str) -> Dict[str, Any]:
    """
    Persist a chat message to the database.

    Args:
        user_id: The user this conversation belongs to
        sender: 'user' or 'bot'
        message: The message text

    Returns:
        Dict with the saved message data
    """
    if sender not in ('user', 'bot'):
        raise ValueError("sender must be 'user' or 'bot'")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO chat_history (user_id, sender, message, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, sender, message.strip(), timestamp)
        )
        conn.commit()
        return {
            'id': cursor.lastrowid,
            'user_id': user_id,
            'sender': sender,
            'message': message,
            'timestamp': timestamp
        }
    finally:
        conn.close()


def get_chat_history(user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Retrieve the most recent chat messages for a user.

    Args:
        user_id: The user's ID
        limit: Maximum number of messages to return (default 50)

    Returns:
        List of message dicts ordered oldest → newest
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, user_id, sender, message, timestamp
            FROM chat_history
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (user_id, limit)
        )
        rows = cursor.fetchall()
        # Return chronological order (oldest first)
        return [dict(row) for row in reversed(rows)]
    finally:
        conn.close()


def get_recent_messages(user_id: int, limit: int = 10) -> list:
    """
    Return the last `limit` chat messages as lightweight {sender, message} dicts.
    Used to feed conversation context to the chatbot.

    Args:
        user_id: The user's ID
        limit:   How many messages to return (chronological order, oldest first)

    Returns:
        List of {'sender': str, 'message': str} dicts
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT sender, message
            FROM chat_history
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (user_id, limit)
        )
        rows = cursor.fetchall()
        return [{'sender': r['sender'], 'message': r['message']} for r in reversed(rows)]
    finally:
        conn.close()


def clear_chat_history(user_id: int) -> int:
    """
    Delete all chat history for a user.

    Args:
        user_id: The user's ID

    Returns:
        Number of rows deleted
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()


# ===== STARTUP =====

if __name__ == '__main__':
    init_db()
    print(f"Database ready at: {DB_PATH}")
