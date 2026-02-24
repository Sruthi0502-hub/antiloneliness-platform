"""
helpers.py – Sentimate
Shared utility functions for app.py route handlers.
Keeps route code thin and consistent.
"""

import io
import base64
import logging
from typing import Any, Dict, Optional, Tuple

from flask import request, jsonify, session

logger = logging.getLogger(__name__)


# ── JSON helpers ─────────────────────────────────────────────────────────────

def parse_json_body() -> Tuple[Optional[Dict[str, Any]], Any]:
    """
    Safely parse the JSON request body.

    Returns:
        (data_dict, None)           on success
        (None, error_response)      when body is missing or not JSON
    """
    try:
        data = request.get_json(force=False, silent=True)
    except Exception:
        data = None

    if data is None:
        return None, (jsonify({'error': 'Request body must be valid JSON', 'code': 400}), 400)
    return data, None


# ── Error response helper ─────────────────────────────────────────────────────

def api_err(message: str, status: int = 400):
    """Return a consistent JSON error response tuple for use in route handlers."""
    return jsonify({'error': message, 'code': status}), status


# ── Language preference ───────────────────────────────────────────────────────

def get_user_language(user_id: Optional[int] = None) -> str:
    """
    Return the current user's language preference.
    Checks session first, then falls back to DB, then defaults to 'english'.
    Caches the result in the session for subsequent calls.
    """
    lang = session.get('lang_pref')
    if lang:
        return lang

    if user_id:
        try:
            from database import get_user_preference
            lang = get_user_preference(user_id, 'language', 'english')
        except Exception as exc:
            logger.warning("Could not fetch language preference for user %s: %s", user_id, exc)
            lang = 'english'
    else:
        lang = 'english'

    session['lang_pref'] = lang
    return lang


# ── Text-to-Speech ────────────────────────────────────────────────────────────

LANG_CODE_MAP: Dict[str, str] = {
    'tamil':   'ta',
    'english': 'en',
}


def text_to_speech_b64(text: str, language: str = 'english') -> str:
    """
    Convert *text* to a gTTS MP3 and return it as a base64-encoded string.

    Args:
        text:     The text to synthesise.
        language: 'english' or 'tamil' (any unrecognised value falls back to 'en').

    Returns:
        Base64-encoded MP3 bytes as a UTF-8 string.

    Raises:
        ImportError: If gTTS is not installed.
        Exception:   If synthesis fails.
    """
    from gtts import gTTS  # deferred import – not required for most routes

    lang_code = LANG_CODE_MAP.get(language.lower(), 'en')
    tts = gTTS(text=text, lang=lang_code, slow=False)

    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


# ── Module availability probe ─────────────────────────────────────────────────

def check_module(module_name: str, symbol: Optional[str] = None) -> bool:
    """
    Try to import *module_name* (and optionally a specific *symbol* from it).
    Returns True if successful, False otherwise. Logs import errors at DEBUG.
    """
    try:
        mod = __import__(module_name)
        if symbol:
            getattr(mod, symbol)
        return True
    except (ImportError, AttributeError) as exc:
        logger.debug("Module probe failed – %s.%s: %s", module_name, symbol or '*', exc)
        return False
