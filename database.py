"""
database.py – Sentimate
SQLite data layer: connection management, schema init, and all CRUD operations.

Improvements:
  - WAL journal mode for better concurrent read performance
  - Index on chat_history(user_id) and reminders(user_id)
  - Context-manager helper _db() to guarantee connection close
  - Explicit PRAGMA journal_mode=WAL and synchronous=NORMAL
  - Consistent logging instead of bare print
  - Capped chat_history auto-prune (keeps latest N rows per user)
"""

import sqlite3
import logging
import os
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ── Configuration ─────────────────────────────────────────────────────────────

DB_PATH = os.environ.get('DB_PATH', 'data/sentimate.db')

# Maximum chat messages stored per user before old ones are pruned
CHAT_HISTORY_MAX = int(os.environ.get('CHAT_HISTORY_MAX', 500))


# ── Connection ────────────────────────────────────────────────────────────────

@contextmanager
def _db():
    """
    Context manager for SQLite connections.
    Guarantees the connection is always closed, even on exceptions.

    Usage:
        with _db() as conn:
            conn.execute(...)
    """
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, isolation_level=None)  # autocommit off via BEGIN
    conn.row_factory = sqlite3.Row
    try:
        # Performance & safety PRAGMAs
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_connection() -> sqlite3.Connection:
    """
    Create and return a raw SQLite connection (legacy compatibility shim).
    Prefer using the _db() context manager for new code.
    """
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


# ── Schema Init ───────────────────────────────────────────────────────────────

def init_db() -> None:
    """
    Create all required tables and indexes if they do not already exist.
    Safe to call on every application startup.
    """
    with _db() as conn:
        conn.executescript("""
            BEGIN;

            -- Users
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT    NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT    NOT NULL,
                created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
            );

            -- Medication reminders
            CREATE TABLE IF NOT EXISTS reminders (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                medicine_name TEXT    NOT NULL,
                time          TEXT    NOT NULL,
                created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
            );

            -- Chat history
            CREATE TABLE IF NOT EXISTS chat_history (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id   INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                sender    TEXT    NOT NULL CHECK(sender IN ('user', 'bot')),
                message   TEXT    NOT NULL,
                timestamp TEXT    NOT NULL DEFAULT (datetime('now'))
            );

            -- User preferences (language etc.)
            CREATE TABLE IF NOT EXISTS user_preferences (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                pref_key   TEXT    NOT NULL,
                pref_value TEXT    NOT NULL,
                updated_at TEXT    NOT NULL DEFAULT (datetime('now')),
                UNIQUE(user_id, pref_key)
            );

            -- Indexes for common query patterns
            CREATE INDEX IF NOT EXISTS idx_reminders_user
                ON reminders(user_id);
            CREATE INDEX IF NOT EXISTS idx_chat_history_user
                ON chat_history(user_id, id DESC);
            CREATE INDEX IF NOT EXISTS idx_user_pref_lookup
                ON user_preferences(user_id, pref_key);

            COMMIT;
        """)
    logger.info("Database initialised – %s", DB_PATH)


# ── User Preferences ──────────────────────────────────────────────────────────

def save_user_preference(user_id: int, pref_key: str, pref_value: str) -> None:
    """Upsert a user preference key/value pair."""
    with _db() as conn:
        conn.execute(
            """
            INSERT INTO user_preferences (user_id, pref_key, pref_value, updated_at)
            VALUES (?, ?, ?, datetime('now'))
            ON CONFLICT(user_id, pref_key) DO UPDATE SET
                pref_value = excluded.pref_value,
                updated_at = excluded.updated_at
            """,
            (user_id, pref_key, str(pref_value))
        )
        conn.commit()


def get_user_preference(user_id: int, pref_key: str, default: str = None) -> Optional[str]:
    """Retrieve a single user preference value, or *default* if not found."""
    with _db() as conn:
        row = conn.execute(
            "SELECT pref_value FROM user_preferences WHERE user_id = ? AND pref_key = ?",
            (user_id, pref_key)
        ).fetchone()
        return row['pref_value'] if row else default


# ── Users ────────────────────────────────────────────────────────────────────

def create_user(username: str, password_hash: str) -> Dict[str, Any]:
    """
    Insert a new user. Returns {'id': int, 'username': str}.
    Raises ValueError if the username is already taken.
    """
    try:
        with _db() as conn:
            cur = conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username.strip(), password_hash)
            )
            conn.commit()
            return {'id': cur.lastrowid, 'username': username.strip()}
    except sqlite3.IntegrityError:
        raise ValueError(f"Username '{username}' is already taken.")


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Return user dict for the given username (case-insensitive), or None."""
    with _db() as conn:
        row = conn.execute(
            "SELECT id, username, password_hash, created_at FROM users WHERE username = ? COLLATE NOCASE",
            (username.strip(),)
        ).fetchone()
        return dict(row) if row else None


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Return user dict by primary key (excludes password_hash), or None."""
    with _db() as conn:
        row = conn.execute(
            "SELECT id, username, created_at FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
        return dict(row) if row else None


# ── Reminders ────────────────────────────────────────────────────────────────

def add_reminder_db(user_id: int, medicine_name: str, time: str) -> Dict[str, Any]:
    """Insert a medication reminder. Returns the created record as a dict."""
    with _db() as conn:
        cur = conn.execute(
            "INSERT INTO reminders (user_id, medicine_name, time) VALUES (?, ?, ?)",
            (user_id, medicine_name.strip(), time.strip())
        )
        conn.commit()
        return {
            'id':            cur.lastrowid,
            'user_id':       user_id,
            'medicine_name': medicine_name.strip(),
            'time':          time.strip(),
        }


def get_reminders_for_user(user_id: int) -> List[Dict[str, Any]]:
    """Return all reminders for a user, ordered by time ascending."""
    with _db() as conn:
        rows = conn.execute(
            "SELECT id, user_id, medicine_name, time, created_at "
            "FROM reminders WHERE user_id = ? ORDER BY time ASC",
            (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]


def delete_reminder_db(reminder_id: int, user_id: int) -> bool:
    """
    Delete a reminder. The user_id check prevents deleting another user's data.
    Returns True if the row was deleted, False if not found.
    """
    with _db() as conn:
        cur = conn.execute(
            "DELETE FROM reminders WHERE id = ? AND user_id = ?",
            (reminder_id, user_id)
        )
        conn.commit()
        return cur.rowcount > 0


# ── Chat History ─────────────────────────────────────────────────────────────

def save_message(user_id: int, sender: str, message: str) -> Dict[str, Any]:
    """
    Persist a chat message and auto-prune old messages beyond CHAT_HISTORY_MAX.

    Args:
        sender: 'user' or 'bot'
    """
    if sender not in ('user', 'bot'):
        raise ValueError("sender must be 'user' or 'bot'")

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with _db() as conn:
        cur = conn.execute(
            "INSERT INTO chat_history (user_id, sender, message, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, sender, message.strip(), timestamp)
        )
        conn.commit()

        # Prune oldest rows when limit exceeded (keep latest CHAT_HISTORY_MAX)
        conn.execute(
            """
            DELETE FROM chat_history
            WHERE user_id = ? AND id NOT IN (
                SELECT id FROM chat_history
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT ?
            )
            """,
            (user_id, user_id, CHAT_HISTORY_MAX)
        )
        conn.commit()

        return {
            'id':        cur.lastrowid,
            'user_id':   user_id,
            'sender':    sender,
            'message':   message.strip(),
            'timestamp': timestamp,
        }


def get_chat_history(user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Return the most recent *limit* messages for a user, oldest first.
    """
    limit = max(1, min(limit, 500))  # clamp between 1 and 500
    with _db() as conn:
        rows = conn.execute(
            """
            SELECT id, user_id, sender, message, timestamp
            FROM chat_history
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (user_id, limit)
        ).fetchall()
        return [dict(r) for r in reversed(rows)]


def get_recent_messages(user_id: int, limit: int = 10) -> list:
    """
    Return lightweight {'sender', 'message'} dicts for chatbot context.
    Oldest first.
    """
    limit = max(1, min(limit, 50))
    with _db() as conn:
        rows = conn.execute(
            """
            SELECT sender, message
            FROM chat_history
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (user_id, limit)
        ).fetchall()
        return [{'sender': r['sender'], 'message': r['message']} for r in reversed(rows)]


def clear_chat_history(user_id: int) -> int:
    """Delete all chat history for a user. Returns number of rows deleted."""
    with _db() as conn:
        cur = conn.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
        conn.commit()
        return cur.rowcount


# ── Startup ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    init_db()
    print(f"Database ready at: {DB_PATH}")
