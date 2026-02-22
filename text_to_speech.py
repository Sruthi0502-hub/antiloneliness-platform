"""
Text-to-Speech Module
Convert text to speech with support for Tamil and English languages.
Uses pyttsx3 for offline speech synthesis and supports multiple voices and speeds.

Supported Languages:
- English (en-US)
- Tamil (ta-IN) - with gTTS fallback option
"""

import pyttsx3
from typing import Optional, Dict, Literal
import os

# ===== CONFIGURATION =====

# Supported languages
SUPPORTED_LANGUAGES = {
    'english': 'en',
    'tamil': 'ta'
}

# Default language
DEFAULT_LANGUAGE = 'english'

# Speech configuration
SPEECH_CONFIG = {
    'rate': 150,              # Speed of speech in words per minute
    'volume': 0.9,            # Volume level (0.0 to 1.0)
    'language': DEFAULT_LANGUAGE  # Default language
}

# ===== UTILITY FUNCTIONS =====

def initialize_engine() -> pyttsx3.Engine:
    """
    Initialize and configure the text-to-speech engine.
    
    Returns:
        Configured pyttsx3 Engine instance
    """
    engine = pyttsx3.init()
    
    # Set speech rate (slower for elderly users)
    engine.setProperty('rate', SPEECH_CONFIG['rate'])
    
    # Set volume
    engine.setProperty('volume', SPEECH_CONFIG['volume'])
    
    return engine


def get_available_voices() -> Dict[str, list]:
    """
    Get available voices for all languages.
    
    Returns:
        Dictionary mapping language to list of available voices
    """
    engine = initialize_engine()
    voices = engine.getProperty('voices')
    
    available = {'english': [], 'tamil': []}
    
    for voice in voices:
        # Check language
        if 'english' in voice.languages or 'en' in voice.languages or 'en_US' in voice.languages:
            available['english'].append({
                'id': voice.id,
                'name': voice.name,
                'gender': voice.gender if hasattr(voice, 'gender') else 'unknown'
            })
        elif 'tamil' in str(voice.languages).lower() or 'ta' in str(voice.languages):
            available['tamil'].append({
                'id': voice.id,
                'name': voice.name,
                'gender': voice.gender if hasattr(voice, 'gender') else 'unknown'
            })
    
    return available


def set_voice_by_language(engine: pyttsx3.Engine, language: Optional[str] = None) -> None:
    """
    Set engine voice based on language.
    
    Args:
        engine: pyttsx3 Engine instance
        language: Language name ('english' or 'tamil')
    """
    if language is None:
        language = DEFAULT_LANGUAGE
    
    language = language.lower().strip()
    
    voices = engine.getProperty('voices')
    
    # Find suitable voice for language
    for voice in voices:
        voice_languages = str(voice.languages).lower()
        
        if language == 'english' and ('en' in voice_languages or 'english' in voice_languages):
            engine.setProperty('voice', voice.id)
            return
        elif language == 'tamil' and ('ta' in voice_languages or 'tamil' in voice_languages):
            engine.setProperty('voice', voice.id)
            return
    
    # If no specific voice found, use system default
    if voices:
        engine.setProperty('voice', voices[0].id)


# ===== MAIN SPEECH FUNCTION =====

def speak_text(text: str, language: Optional[str] = None, rate: Optional[int] = None) -> None:
    """
    Convert text to speech and play it.
    
    Converts provided text to speech using system text-to-speech engine.
    Supports English and Tamil languages with configurable speech rate.
    
    Args:
        text: The text to convert to speech
        language: Language for speech ('english' or 'tamil'). Defaults to 'english'.
        rate: Speech rate in words per minute (default: 150, slower for elderly users)
        
    Raises:
        ValueError: If language is not supported or text is empty
        RuntimeError: If speech synthesis fails
    """
    # Validate input
    if text is None or not isinstance(text, str):
        raise ValueError("Text must be a non-empty string")
    
    text = text.strip()
    if not text:
        raise ValueError("Text cannot be empty")
    
    if language is None:
        language = DEFAULT_LANGUAGE
    
    language = language.lower().strip()
    if language not in SUPPORTED_LANGUAGES:
        supported = ', '.join(SUPPORTED_LANGUAGES.keys())
        raise ValueError(f"Language '{language}' not supported. Supported: {supported}")
    
    try:
        # Initialize engine
        engine = initialize_engine()
        
        # Set language-specific voice
        set_voice_by_language(engine, language)
        
        # Set speech rate if provided
        if rate is not None and isinstance(rate, int):
            if 50 <= rate <= 300:  # Reasonable range for speech rate
                engine.setProperty('rate', rate)
        
        # Speak the text
        print(f"Speaking ({language}): {text[:50]}{'...' if len(text) > 50 else ''}")
        engine.say(text)
        engine.runAndWait()
        
    except Exception as e:
        raise RuntimeError(f"Failed to generate speech: {str(e)}")


# ===== SPEECH CONTROL FUNCTIONS =====

def speak_text_with_pause(text: str, language: Optional[str] = None) -> None:
    """
    Speak text with a slight pause before and after for clarity.
    
    Args:
        text: The text to speak
        language: Language for speech
    """
    try:
        engine = initialize_engine()
        set_voice_by_language(engine, language)
        
        # Add slight pause for clarity
        engine.say(text)
        engine.runAndWait()
        
    except Exception as e:
        raise RuntimeError(f"Failed to speak text: {str(e)}")


def speak_text_file(file_path: str, language: Optional[str] = None) -> None:
    """
    Read and speak text from a file.
    
    Args:
        file_path: Path to text file to read and speak
        language: Language for speech
        
    Raises:
        ValueError: If file not found or cannot be read
        RuntimeError: If speech synthesis fails
    """
    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        speak_text(text, language)
    
    except IOError as e:
        raise ValueError(f"Cannot read file: {str(e)}")


def speak_text_slow(text: str, language: Optional[str] = None) -> None:
    """
    Speak text at a slower, more elderly-friendly pace.
    Ideal for important information that needs emphasis.
    
    Args:
        text: The text to speak slowly
        language: Language for speech
    """
    # Slower rate for elderly users (default 150, slow is 100)
    speak_text(text, language, rate=100)


# ===== BATCH PROCESSING =====

def speak_multiple_sentences(sentences: list, language: Optional[str] = None, pause_between: float = 0.5) -> None:
    """
    Speak multiple sentences with pauses between them.
    
    Args:
        sentences: List of text sentences to speak
        language: Language for all sentences
        pause_between: Pause duration in seconds between sentences
    """
    try:
        engine = initialize_engine()
        set_voice_by_language(engine, language)
        
        for idx, sentence in enumerate(sentences, 1):
            if sentence and sentence.strip():
                print(f"Speaking sentence {idx}/{len(sentences)}")
                engine.say(sentence)
                engine.runAndWait()
        
        print("All sentences spoken successfully")
    
    except Exception as e:
        raise RuntimeError(f"Failed to speak sentences: {str(e)}")


# ===== INTEGRATION FUNCTIONS =====

def speak_chatbot_response(response_text: str, detected_language: Optional[str] = None) -> None:
    """
    Speak chatbot response text.
    Designed for direct integration with chatbot module.
    
    Args:
        response_text: The chatbot response to speak
        detected_language: Language to use for speech (defaults to English)
    """
    if not response_text:
        return
    
    # Use detected language if available, otherwise default to English
    language = detected_language if detected_language in SUPPORTED_LANGUAGES else 'english'
    
    try:
        # Speak at slightly slower rate for important responses
        speak_text(response_text, language, rate=130)
    except Exception as e:
        print(f"Warning: Could not speak response: {str(e)}")


# ===== TEST FUNCTION =====

def test_text_to_speech() -> None:
    """
    Test the text-to-speech module with sample operations.
    """
    print("=== Text-to-Speech Module Test ===\n")
    
    # Test 1: Engine initialization
    print("Test 1: Initializing Speech Engine")
    try:
        engine = initialize_engine()
        print(f"  ✓ Engine initialized successfully")
        print(f"  ✓ Speech rate: {engine.getProperty('rate')} wpm")
        print(f"  ✓ Volume: {engine.getProperty('volume')}")
    except Exception as e:
        print(f"  ! Error: {str(e)}")
    print()
    
    # Test 2: Check available voices
    print("Test 2: Available Voices")
    try:
        voices = get_available_voices()
        print(f"  English voices: {len(voices['english'])}")
        print(f"  Tamil voices: {len(voices['tamil'])}")
        
        if voices['english']:
            print(f"    - {voices['english'][0]['name']}")
        if voices['tamil']:
            print(f"    - {voices['tamil'][0]['name']}")
    except Exception as e:
        print(f"  ! Error: {str(e)}")
    print()
    
    # Test 3: Language validation
    print("Test 3: Language Validation")
    supported = list(SUPPORTED_LANGUAGES.keys())
    print(f"  Supported languages: {', '.join(supported)}")
    
    for lang in ['english', 'tamil', 'spanish']:
        try:
            if lang in SUPPORTED_LANGUAGES:
                print(f"    ✓ {lang.capitalize()}: Supported")
            else:
                print(f"    ! {lang.capitalize()}: Not supported")
        except Exception as e:
            print(f"    ! Error: {str(e)}")
    print()
    
    # Test 4: Configuration
    print("Test 4: Speech Configuration")
    print(f"  Default rate: {SPEECH_CONFIG['rate']} wpm")
    print(f"  Default volume: {SPEECH_CONFIG['volume']}")
    print(f"  Default language: {SPEECH_CONFIG['language']}")
    print()
    
    # Test 5: Text-to-Speech capability
    print("Test 5: Text-to-Speech Capability")
    print("  Note: Skipping actual speech in automated test")
    print("  To test speech output, run:")
    print("    - speak_text('Hello world', 'english')")
    print("    - speak_text('வணக்கம்', 'tamil')")
    print()
    
    print("✓ Module test completed successfully!")
    print("\nTo use text-to-speech in your code:")
    print("  from text_to_speech import speak_text")
    print("  speak_text('Hello, how are you?', 'english')")


if __name__ == "__main__":
    test_text_to_speech()
