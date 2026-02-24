"""
auth.py – Sentimate
User registration and authentication.

Security:
  - werkzeug PBKDF2-SHA256 password hashing (cost factor 260k iterations by default)
  - Generic login error message to prevent username enumeration
  - Stronger password rules (min 8 chars, requires letter + digit)
  - Username: alpha-numeric + hyphen/underscore, 3–30 chars
"""

import re
import logging
from typing import Dict, Any, Optional, Tuple

from werkzeug.security import generate_password_hash, check_password_hash

from database import create_user, get_user_by_username

logger = logging.getLogger(__name__)


# ── Constants ─────────────────────────────────────────────────────────────────

MIN_USERNAME_LEN = 3
MAX_USERNAME_LEN = 30
MIN_PASSWORD_LEN = 8          # increased from 6

_USERNAME_RE = re.compile(r'^[A-Za-z0-9_-]+$')


# ── Validators ────────────────────────────────────────────────────────────────

def _validate_username(username: str) -> Optional[str]:
    """Return an error string or None."""
    if not username:
        return "Username is required."
    if len(username) < MIN_USERNAME_LEN:
        return f"Username must be at least {MIN_USERNAME_LEN} characters."
    if len(username) > MAX_USERNAME_LEN:
        return f"Username must be at most {MAX_USERNAME_LEN} characters."
    if not _USERNAME_RE.match(username):
        return "Username may only contain letters, numbers, hyphens, and underscores."
    return None


def _validate_password(password: str) -> Optional[str]:
    """Return an error string or None."""
    if not password:
        return "Password is required."
    if len(password) < MIN_PASSWORD_LEN:
        return f"Password must be at least {MIN_PASSWORD_LEN} characters."
    if not re.search(r'[A-Za-z]', password):
        return "Password must contain at least one letter."
    if not re.search(r'[0-9]', password):
        return "Password must contain at least one number."
    return None


# ── Registration ──────────────────────────────────────────────────────────────

def register_user(
    username: str,
    password: str,
    confirm_password: str,
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Validate fields, hash the password, and create a new user account.

    Returns:
        (True, success_message, user_dict)  on success
        (False, error_message, None)        on failure
    """
    username = username.strip()

    err = _validate_username(username)
    if err:
        return False, err, None

    err = _validate_password(password)
    if err:
        return False, err, None

    if password != confirm_password:
        return False, "Passwords do not match.", None

    try:
        password_hash = generate_password_hash(password)
        user = create_user(username, password_hash)
        logger.info("New user registered: %s (id=%s)", username, user['id'])
        return True, "Account created successfully! Please log in.", user

    except ValueError as exc:
        return False, str(exc), None

    except Exception as exc:
        logger.error("Registration failed for username '%s': %s", username, exc)
        return False, "Registration failed. Please try again.", None


# ── Authentication ────────────────────────────────────────────────────────────

_INVALID_CREDS_MSG = "Invalid username or password."


def authenticate_user(
    username: str,
    password: str,
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Verify credentials and return a safe user dict (no password_hash).

    The same generic error message is returned for both unknown username and
    wrong password to prevent username enumeration.

    Returns:
        (True, success_message, safe_user_dict)  on success
        (False, error_message, None)             on failure
    """
    if not username or not username.strip():
        return False, "Username is required.", None
    if not password:
        return False, "Password is required.", None

    try:
        user = get_user_by_username(username.strip())
    except Exception as exc:
        logger.error("Database error during authentication: %s", exc)
        return False, "Login failed. Please try again.", None

    # Generic message for both "not found" and "wrong password"
    if user is None or not check_password_hash(user['password_hash'], password):
        logger.warning(
            "Failed login attempt for username '%s'",
            username.strip(),
        )
        return False, _INVALID_CREDS_MSG, None

    safe_user = {
        'id':         user['id'],
        'username':   user['username'],
        'created_at': user['created_at'],
    }
    logger.info("User authenticated: %s (id=%s)", safe_user['username'], safe_user['id'])
    return True, "Login successful!", safe_user
