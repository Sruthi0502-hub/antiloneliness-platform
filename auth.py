"""
Authentication Module for Sentimate
Handles user registration, login validation, and password security.

Uses werkzeug's security helpers for safe password hashing (pbkdf2:sha256).
"""

from typing import Optional, Dict, Any, Tuple
from werkzeug.security import generate_password_hash, check_password_hash
from database import create_user, get_user_by_username


# ===== VALIDATION HELPERS =====

MIN_USERNAME_LEN = 3
MAX_USERNAME_LEN = 30
MIN_PASSWORD_LEN = 6


def _validate_username(username: str) -> Optional[str]:
    """Return an error string if username is invalid, else None."""
    username = username.strip()
    if not username:
        return "Username is required."
    if len(username) < MIN_USERNAME_LEN:
        return f"Username must be at least {MIN_USERNAME_LEN} characters."
    if len(username) > MAX_USERNAME_LEN:
        return f"Username must be at most {MAX_USERNAME_LEN} characters."
    if not username.replace('_', '').replace('-', '').isalnum():
        return "Username can only contain letters, numbers, hyphens, and underscores."
    return None


def _validate_password(password: str) -> Optional[str]:
    """Return an error string if password is invalid, else None."""
    if not password:
        return "Password is required."
    if len(password) < MIN_PASSWORD_LEN:
        return f"Password must be at least {MIN_PASSWORD_LEN} characters."
    return None


# ===== REGISTRATION =====

def register_user(username: str, password: str, confirm_password: str) -> Tuple[bool, str, Optional[Dict]]:
    """
    Register a new user account.

    Args:
        username: Desired username
        password: Chosen password
        confirm_password: Password confirmation

    Returns:
        (success: bool, message: str, user_data: dict | None)
    """
    # Validate username
    err = _validate_username(username)
    if err:
        return False, err, None

    # Validate password
    err = _validate_password(password)
    if err:
        return False, err, None

    # Confirm passwords match
    if password != confirm_password:
        return False, "Passwords do not match.", None

    # Hash password and create account
    try:
        password_hash = generate_password_hash(password)
        user = create_user(username.strip(), password_hash)
        return True, "Account created successfully! Please log in.", user
    except ValueError as e:
        return False, str(e), None
    except Exception as e:
        return False, f"Registration failed: {str(e)}", None


# ===== LOGIN =====

def authenticate_user(username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
    """
    Verify login credentials.

    Args:
        username: Username to authenticate
        password: Plain-text password to verify

    Returns:
        (success: bool, message: str, user_data: dict | None)
    """
    if not username or not username.strip():
        return False, "Username is required.", None

    if not password:
        return False, "Password is required.", None

    user = get_user_by_username(username.strip())

    if user is None:
        return False, "Invalid username or password.", None

    if not check_password_hash(user['password_hash'], password):
        return False, "Invalid username or password.", None

    # Return safe user data (no password hash)
    safe_user = {
        'id': user['id'],
        'username': user['username'],
        'created_at': user['created_at']
    }
    return True, "Login successful!", safe_user
