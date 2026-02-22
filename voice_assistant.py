"""
Voice Assistant Module for Sentimate
Speech-to-text supporting English and Tamil using Google Speech Recognition.

Main public function:
    listen_voice(language='english', timeout=5, phrase_time_limit=15)
        → Returns the detected text string (or empty string on failure)
"""

import speech_recognition as sr
from typing import Optional


# ============================================================
# LANGUAGE CONFIGURATION
# ============================================================

LANGUAGE_CODES = {
    'english': 'en-US',
    'tamil':   'ta-IN',
    'en':      'en-US',
    'ta':      'ta-IN',
    'en-us':   'en-US',
    'ta-in':   'ta-IN',
}


def get_language_code(language: str) -> str:
    """Return BCP-47 language code for the given language name (backward-compat alias)."""
    return LANGUAGE_CODES.get(language.lower().strip(), 'en-US')


# ============================================================
# PUBLIC API
# ============================================================

def listen_voice(
    language: str = 'english',
    timeout: int = 5,
    phrase_time_limit: int = 15,
    energy_threshold: int = 300,
    dynamic_energy: bool = True,
) -> str:
    """
    Listen to the microphone and return the detected speech as text.

    Supports English (en-US) and Tamil (ta-IN) via Google Speech Recognition.

    Args:
        language:          'english' or 'tamil' (case-insensitive).
                           Also accepts BCP-47 codes like 'en-US', 'ta-IN'.
        timeout:           Seconds to wait for speech to start. 0 = no limit.
        phrase_time_limit: Maximum seconds to record a single phrase.
        energy_threshold:  Minimum audio energy to treat as speech.
        dynamic_energy:    Allow recogniser to auto-adjust energy threshold.

    Returns:
        Detected text string (stripped), or '' on any failure.
    """
    lang_key = language.lower().strip()
    lang_code = LANGUAGE_CODES.get(lang_key, 'en-US')

    recogniser = sr.Recognizer()
    recogniser.energy_threshold = energy_threshold
    recogniser.dynamic_energy_threshold = dynamic_energy
    recogniser.pause_threshold = 0.8  # seconds of silence to end phrase

    try:
        with sr.Microphone() as source:
            # Adjust for ambient noise (half a second)
            recogniser.adjust_for_ambient_noise(source, duration=0.5)

            # Listen — timeout applies to start-of-speech; phrase_time_limit caps recording
            listen_kwargs = {'phrase_time_limit': phrase_time_limit}
            if timeout and timeout > 0:
                listen_kwargs['timeout'] = timeout

            audio = recogniser.listen(source, **listen_kwargs)

        # Attempt recognition using Google Web Speech API
        text = recogniser.recognize_google(audio, language=lang_code)
        return text.strip()

    except sr.WaitTimeoutError:
        # No speech detected within timeout window — not an error, just silence
        return ''

    except sr.UnknownValueError:
        # Audio was captured but could not be understood
        return ''

    except sr.RequestError as e:
        # Could not reach Google's API (network issue)
        print(f"[voice_assistant] Google Speech API error: {e}")
        return ''

    except OSError as e:
        # No microphone found or permission denied
        print(f"[voice_assistant] Microphone error: {e}")
        return ''

    except Exception as e:
        print(f"[voice_assistant] Unexpected error: {e}")
        return ''


def listen_once(language: str = 'english') -> str:
    """Convenience alias — listen with default settings."""
    return listen_voice(language=language)


def listen_continuously(
    language: str = 'english',
    callback=None,
    max_iterations: int = 10,
) -> None:
    """
    Continuously listen and call callback(text) for each detected phrase.

    Args:
        language:       Target language.
        callback:       Callable that receives the detected string.
                        If None, prints to stdout.
        max_iterations: Safety limit on how many phrases to capture.
    """
    if callback is None:
        callback = lambda text: print(f"Detected: {text}")

    print(f"[voice_assistant] Continuous listening ({language}). Max {max_iterations} phrases.")
    for _ in range(max_iterations):
        text = listen_voice(language=language, timeout=0)
        if text:
            callback(text)


# ============================================================
# LOW-LEVEL HELPER (for Flask/web use where mic is client-side)
# ============================================================

def transcribe_audio_bytes(
    audio_bytes: bytes,
    language: str = 'english',
) -> str:
    """
    Transcribe raw WAV audio bytes (useful for server-side audio uploads).

    Args:
        audio_bytes: Raw WAV audio data as bytes.
        language:    Target language key.

    Returns:
        Transcribed text or ''.
    """
    lang_code = LANGUAGE_CODES.get(language.lower(), 'en-US')
    recogniser = sr.Recognizer()
    try:
        import io
        audio_file = sr.AudioFile(io.BytesIO(audio_bytes))
        with audio_file as source:
            audio = recogniser.record(source)
        return recogniser.recognize_google(audio, language=lang_code).strip()
    except Exception as e:
        print(f"[voice_assistant] transcribe_audio_bytes error: {e}")
        return ''


# ============================================================
# CLI TEST
# ============================================================

if __name__ == '__main__':
    import sys

    lang = sys.argv[1] if len(sys.argv) > 1 else 'english'
    print(f"[voice_assistant] Listening in {lang}... (speak now)")

    result = listen_voice(language=lang, timeout=8)

    if result:
        print(f"✓ Detected: {result}")
    else:
        print("✗ No speech detected or recognition failed.")
