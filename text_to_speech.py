"""
Text-to-Speech Module for Sentimate
Converts text to speech, supporting both Tamil and English.

Primary function:
    speak_text(text, language='english') — browser-safe gTTS version (returns base64 MP3)
    speak_text_server(text, language)    — server-console version using pyttsx3 fallback

The Flask app uses the /speak_response endpoint (in app.py) for browser TTS.
This module provides the speak_text() function that can be imported and used
directly in Python scripts or the voice chatbot integration.
"""

import io
import base64
from typing import Optional

# ============================================================
# LANGUAGE CONFIGURATION
# ============================================================

LANGUAGE_CODES = {
    'english': 'en',
    'tamil':   'ta',
    'en':      'en',
    'ta':      'ta',
    'en-us':   'en',
    'ta-in':   'ta',
}

DEFAULT_LANGUAGE = 'english'


def _get_lang_code(language: str) -> str:
    """Return gTTS language code for the given language name."""
    return LANGUAGE_CODES.get(language.lower().strip(), 'en')


# ============================================================
# PRIMARY API — gTTS (browser-compatible, works for Tamil)
# ============================================================

def speak_text(text: str, language: str = 'english') -> Optional[str]:
    """
    Convert text to speech using gTTS and return a base64-encoded MP3 string.

    This is the primary TTS function for the Sentimate platform.
    Supports both English and Tamil.

    Args:
        text:     The text to speak.
        language: 'english' or 'tamil' (also accepts 'en', 'ta', BCP-47 codes).

    Returns:
        Base64-encoded MP3 audio string (suitable for embedding in HTML audio src),
        or None if conversion fails.

    Usage in browser (via Flask):
        audio_b64 = speak_text("Hello!", "english")
        # Use with: <audio src="data:audio/mpeg;base64,{audio_b64}">

    Usage in Python script:
        audio_b64 = speak_text("வணக்கம்!", "tamil")
        if audio_b64:
            # Save to file or stream
    """
    try:
        from gtts import gTTS

        if not text or not text.strip():
            return None

        lang_code = _get_lang_code(language)
        tts = gTTS(text=text.strip(), lang=lang_code, slow=False)

        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')

    except ImportError:
        print("[text_to_speech] gTTS not installed. Run: pip install gTTS")
        return None
    except Exception as e:
        print(f"[text_to_speech] speak_text error: {e}")
        return None


def speak_text_slow(text: str, language: str = 'english') -> Optional[str]:
    """
    Same as speak_text() but with slower speech rate — better for elderly users.

    Args:
        text:     Text to convert.
        language: Target language.

    Returns:
        Base64-encoded MP3 string, or None on failure.
    """
    try:
        from gtts import gTTS

        if not text or not text.strip():
            return None

        lang_code = _get_lang_code(language)
        tts = gTTS(text=text.strip(), lang=lang_code, slow=True)

        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')

    except Exception as e:
        print(f"[text_to_speech] speak_text_slow error: {e}")
        return None


def speak_text_to_file(text: str, language: str = 'english', filepath: str = 'output.mp3') -> bool:
    """
    Save TTS audio to an MP3 file on disk.

    Args:
        text:     Text to speak.
        language: Target language.
        filepath: Destination file path.

    Returns:
        True on success, False on failure.
    """
    try:
        from gtts import gTTS

        if not text or not text.strip():
            return False

        lang_code = _get_lang_code(language)
        tts = gTTS(text=text.strip(), lang=lang_code, slow=False)
        tts.save(filepath)
        return True

    except Exception as e:
        print(f"[text_to_speech] speak_text_to_file error: {e}")
        return False


# ============================================================
# SERVER-CONSOLE VERSION — pyttsx3 (offline, no Tamil support)
# ============================================================

def speak_text_console(text: str, language: str = 'english', slow: bool = False) -> bool:
    """
    Speak text through the system's speakers using pyttsx3 (offline).
    NOTE: Tamil is NOT supported by pyttsx3 — it falls back to English TTS voice
    and will mispronounce Tamil text. Use speak_text() with the browser for Tamil.

    Args:
        text:     Text to speak.
        language: Language hint (affects speech rate, not voice for Tamil).
        slow:     Use slow speech rate (default: False).

    Returns:
        True on success, False on failure.
    """
    try:
        import pyttsx3

        if not text or not text.strip():
            return False

        engine = pyttsx3.init()
        engine.setProperty('volume', 0.9)
        engine.setProperty('rate', 120 if slow else 150)
        engine.say(text.strip())
        engine.runAndWait()
        engine.stop()
        return True

    except Exception as e:
        print(f"[text_to_speech] speak_text_console error: {e}")
        return False


# ============================================================
# LANGUAGE UTILITIES
# ============================================================

def get_supported_languages() -> dict:
    """Return a dict of supported language names and their gTTS codes."""
    return {'english': 'en', 'tamil': 'ta'}


def is_language_supported(language: str) -> bool:
    """Check if a language is supported by speak_text()."""
    return language.lower().strip() in LANGUAGE_CODES


# ============================================================
# CLI TEST
# ============================================================

if __name__ == '__main__':
    import sys

    lang = sys.argv[1] if len(sys.argv) > 1 else 'english'
    texts = {
        'english': 'Hello! This is Sentimate. How are you feeling today?',
        'tamil':   '\u0bb5\u0ba3\u0b95\u0bcd\u0b95\u0bae\u0bcd! \u0b87\u0ba9\u0bcd\u0bb1\u0bc1 \u0b8e\u0baa\u0bcd\u0baa\u0b9f\u0bbf \u0b87\u0bb0\u0bc1\u0b95\u0bcd\u0b95\u0bbf\u0bb1\u0bc0\u0bb0\u0bcd\u0b95\u0bb3\u0bcd?',
    }
    test_text = texts.get(lang, texts['english'])

    print(f"Generating {lang} TTS for: {test_text}")
    audio_b64 = speak_text(test_text, lang)

    if audio_b64:
        out_file = f'test_tts_{lang}.mp3'
        speak_text_to_file(test_text, lang, out_file)
        print(f"✓ Saved to {out_file}")
        print(f"✓ Base64 length: {len(audio_b64)} chars")
    else:
        print("✗ TTS generation failed")
