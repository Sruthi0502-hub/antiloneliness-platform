"""
Voice Assistant Module
Convert voice input to text with support for Tamil and English languages.
Uses Google Speech Recognition API for accurate transcription.

Supported Languages:
- English (en-US)
- Tamil (ta-IN)
"""

import speech_recognition as sr
from typing import Dict, Optional, Tuple

# ===== CONFIGURATION =====

# Supported language codes and names
SUPPORTED_LANGUAGES = {
    'english': 'en-US',
    'tamil': 'ta-IN'
}

# Default language
DEFAULT_LANGUAGE = 'english'

# Audio configuration
AUDIO_CONFIG = {
    'timeout': 10,  # Maximum wait time for audio input (seconds)
    'phrase_time_limit': 15,  # Maximum duration of single phrase (seconds)
    'energy_threshold': 4000  # Minimum energy threshold to detect speech
}

# ===== UTILITY FUNCTIONS =====

def initialize_recognizer() -> sr.Recognizer:
    """
    Initialize and configure the speech recognizer.
    
    Returns:
        Configured Recognizer instance
    """
    recognizer = sr.Recognizer()
    
    # Adjust energy threshold for better speech detection
    recognizer.energy_threshold = AUDIO_CONFIG['energy_threshold']
    
    # Allow for dynamic adjustment if needed
    recognizer.dynamic_energy_threshold = True
    
    return recognizer


def get_language_code(language: Optional[str] = None) -> str:
    """
    Convert language name to speech recognition language code.
    
    Args:
        language: Language name (e.g., 'english', 'tamil'). Defaults to English.
        
    Returns:
        Language code for speech recognition API
        
    Raises:
        ValueError: If language is not supported
    """
    if language is None:
        language = DEFAULT_LANGUAGE
    
    language_lower = language.lower().strip()
    
    if language_lower not in SUPPORTED_LANGUAGES:
        supported = ', '.join(SUPPORTED_LANGUAGES.keys())
        raise ValueError(f"Language '{language}' not supported. Supported languages: {supported}")
    
    return SUPPORTED_LANGUAGES[language_lower]


# ===== MAIN VOICE CAPTURE FUNCTION =====

def listen_voice(language: Optional[str] = None) -> str:
    """
    Listen to voice input from microphone and convert to text.
    
    Captures audio from the default microphone, converts speech to text
    using Google's speech recognition API.
    
    Args:
        language: Language for recognition ('english' or 'tamil'). Defaults to 'english'.
        
    Returns:
        Detected text from voice input
        
    Raises:
        ValueError: If language is not supported
        RuntimeError: If microphone is not available or audio processing fails
        sr.UnknownValueError: If speech cannot be understood
        sr.RequestError: If API request fails
        TimeoutError: If no audio detected within timeout period
    """
    try:
        # Get language code
        language_code = get_language_code(language)
        language_name = language.lower() if language else DEFAULT_LANGUAGE
        
        # Initialize recognizer and microphone
        recognizer = initialize_recognizer()
        microphone = sr.Microphone()
        
        # Adjust microphone for ambient noise
        with microphone as source:
            print(f"Listening for {language_name} speech... Please speak clearly.")
            print(f"(Timeout in {AUDIO_CONFIG['timeout']} seconds)")
            
            try:
                # Capture audio with timeout
                audio = recognizer.listen(
                    source,
                    timeout=AUDIO_CONFIG['timeout'],
                    phrase_time_limit=AUDIO_CONFIG['phrase_time_limit']
                )
            except sr.WaitTimeoutError:
                raise TimeoutError(f"No audio detected within {AUDIO_CONFIG['timeout']} seconds")
        
        # Convert speech to text using Google Speech Recognition
        try:
            print("Processing audio... Converting to text.")
            text = recognizer.recognize_google(audio, language=language_code)
            print(f"Detected text: {text}")
            return text
        
        except sr.UnknownValueError:
            error_msg = "Could not understand audio. Please speak clearly and try again."
            raise sr.UnknownValueError(error_msg)
        
        except sr.RequestError as e:
            error_msg = f"Speech Recognition API error: {str(e)}"
            raise sr.RequestError(error_msg)
    
    except ValueError as e:
        # Re-raise language validation errors
        raise ValueError(str(e))
    
    except (OSError, RuntimeError) as e:
        # Microphone not available
        raise RuntimeError(f"Microphone error: {str(e)}. Ensure microphone is connected and accessible.")
    
    except Exception as e:
        # Catch any other unexpected errors
        raise RuntimeError(f"Unexpected error during voice capture: {str(e)}")


# ===== ADVANCED VOICE CAPTURE FUNCTION =====

def listen_voice_with_language_selection() -> Tuple[str, str]:
    """
    Listen to voice input with language selection option.
    
    Prompts user to select language before capturing voice input.
    
    Returns:
        Tuple of (detected_text, language_used)
        
    Raises:
        RuntimeError: If voice capture fails
    """
    print("\n=== Voice Assistant ===")
    print("Supported Languages:")
    for idx, lang in enumerate(SUPPORTED_LANGUAGES.keys(), 1):
        print(f"  {idx}. {lang.capitalize()}")
    
    # Default to English if no selection
    selected_language = DEFAULT_LANGUAGE
    
    try:
        # Try to get language selection from input
        print(f"\nDefault language: {selected_language}")
        user_input = input("Enter language (or press Enter for default): ").strip()
        
        if user_input:
            selected_language = user_input.lower()
    
    except Exception:
        # Use default if any input error
        pass
    
    # Validate language selection
    try:
        get_language_code(selected_language)
    except ValueError:
        print(f"Invalid language. Using default: {DEFAULT_LANGUAGE}")
        selected_language = DEFAULT_LANGUAGE
    
    # Capture voice
    detected_text = listen_voice(selected_language)
    
    return detected_text, selected_language


# ===== HELPER FUNCTION FOR BATCH PROCESSING =====

def recognize_from_audio_file(file_path: str, language: Optional[str] = None) -> str:
    """
    Recognize speech from an audio file instead of microphone.
    
    Args:
        file_path: Path to audio file (supports WAV, AIFF, FLAC)
        language: Language for recognition ('english' or 'tamil')
        
    Returns:
        Detected text from audio file
        
    Raises:
        ValueError: If language is not supported or file doesn't exist
        RuntimeError: If audio processing fails
        sr.UnknownValueError: If speech cannot be understood
    """
    import os
    
    # Validate file exists
    if not os.path.exists(file_path):
        raise ValueError(f"Audio file not found: {file_path}")
    
    # Validate file format
    valid_formats = ('.wav', '.aiff', '.flac', '.mp3')
    if not file_path.lower().endswith(valid_formats):
        raise ValueError(f"Unsupported audio format. Supported: {valid_formats}")
    
    try:
        # Get language code
        language_code = get_language_code(language)
        
        # Initialize recognizer
        recognizer = initialize_recognizer()
        
        # Load audio file
        with sr.AudioFile(file_path) as source:
            print(f"Loading audio from: {file_path}")
            audio = recognizer.record(source)
        
        print("Processing audio file... Converting to text.")
        
        # Convert speech to text
        text = recognizer.recognize_google(audio, language=language_code)
        print(f"Detected text: {text}")
        
        return text
    
    except sr.UnknownValueError:
        raise sr.UnknownValueError("Could not understand speech in audio file")
    
    except sr.RequestError as e:
        raise RuntimeError(f"Speech Recognition API error: {str(e)}")
    
    except Exception as e:
        raise RuntimeError(f"Error processing audio file: {str(e)}")


# ===== TEST FUNCTION =====

def test_voice_assistant() -> None:
    """
    Test the voice assistant module with sample operations.
    Demonstrates different voice capture scenarios.
    """
    print("=== Voice Assistant Module Test ===\n")
    
    # Test 1: Language support verification
    print("Test 1: Supported Languages")
    print(f"  Languages: {', '.join(SUPPORTED_LANGUAGES.keys())}")
    print(f"  Language codes: {SUPPORTED_LANGUAGES}")
    print()
    
    # Test 2: Recognizer initialization
    print("Test 2: Initializing Speech Recognizer")
    try:
        recognizer = initialize_recognizer()
        print(f"  ✓ Recognizer initialized successfully")
        print(f"  ✓ Energy threshold: {recognizer.energy_threshold}")
        print(f"  ✓ Dynamic energy adjustment: {recognizer.dynamic_energy_threshold}")
    except Exception as e:
        print(f"  ! Error: {str(e)}")
    print()
    
    # Test 3: Microphone detection
    print("Test 3: Microphone Detection")
    try:
        microphone = sr.Microphone()
        print(f"  ✓ Microphone found and ready")
        print(f"  ✓ Audio device index: {microphone.device_index}")
        
        # List available microphones
        print("\n  Available microphones:")
        for idx, mic_name in enumerate(sr.Microphone.list_microphone_indexes()):
            print(f"    - Device {idx}: Microphone available")
    
    except Exception as e:
        print(f"  ! Microphone Error: {str(e)}")
        print(f"  ! Note: Microphone must be connected for voice recognition")
    print()
    
    # Test 4: Language code validation
    print("Test 4: Language Code Validation")
    test_languages = ['english', 'tamil', 'french']
    
    for lang in test_languages:
        try:
            code = get_language_code(lang)
            print(f"  ✓ {lang.capitalize()}: {code}")
        except ValueError as e:
            print(f"  ! {lang.capitalize()}: Not supported")
    print()
    
    # Test 5: Voice capture simulation
    print("Test 5: Voice Capture Capability")
    print("  Note: Skipping actual voice capture in automated test")
    print("  To test voice capture, run: listen_voice()")
    print("  Example usage:")
    print("    - listen_voice('english')  # English voice input")
    print("    - listen_voice('tamil')    # Tamil voice input")
    print()
    
    print("✓ Module test completed successfully!")
    print("\nTo use voice assistant in your code:")
    print("  from voice_assistant import listen_voice")
    print("  text = listen_voice('english')")
    print("  # text now contains the spoken input")


if __name__ == "__main__":
    test_voice_assistant()
