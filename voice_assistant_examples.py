"""
Voice Assistant Integration Examples
Demonstrates how to use the voice_assistant module in the Sentimate platform.
"""

from voice_assistant import listen_voice, listen_voice_with_language_selection, recognize_from_audio_file
from chatbot import get_response

# ===== EXAMPLE 1: Simple English Voice Input =====

def example_english_voice_chat():
    """
    Simple example: Capture English voice, process through chatbot.
    """
    print("=== Example 1: English Voice Chat ===\n")
    
    try:
        # Capture voice in English
        user_voice = listen_voice('english')
        
        # Process through chatbot
        bot_response = get_response(user_voice)
        
        print(f"\nChatbot response: {bot_response}")
        
    except Exception as e:
        print(f"Error: {str(e)}")


# ===== EXAMPLE 2: Tamil Voice Input =====

def example_tamil_voice_chat():
    """
    Example with Tamil language support.
    """
    print("=== Example 2: Tamil Voice Chat ===\n")
    
    try:
        # Capture voice in Tamil
        user_voice = listen_voice('tamil')
        
        print(f"\nDetected Tamil text: {user_voice}")
        print("(Chatbot would process this text for response)")
        
    except Exception as e:
        print(f"Error: {str(e)}")


# ===== EXAMPLE 3: Language Selection =====

def example_voice_with_language_selection():
    """
    Example with user language selection.
    """
    print("=== Example 3: Voice with Language Selection ===\n")
    
    try:
        # Let user select language
        text, language = listen_voice_with_language_selection()
        
        print(f"\nLanguage used: {language}")
        print(f"Captured text: {text}")
        
        # Process with chatbot
        response = get_response(text)
        print(f"Bot response: {response}")
        
    except Exception as e:
        print(f"Error: {str(e)}")


# ===== EXAMPLE 4: Voice From File =====

def example_voice_from_audio_file():
    """
    Example processing audio file instead of microphone.
    Useful for testing and batch processing.
    """
    print("=== Example 4: Audio File Processing ===\n")
    
    # Path to audio file (must be WAV, AIFF, or FLAC format)
    audio_file = "path/to/audio/file.wav"
    
    try:
        # Process audio file in English
        text = recognize_from_audio_file(audio_file, 'english')
        print(f"Recognized text: {text}")
        
    except ValueError as e:
        print(f"File error: {str(e)}")
    except Exception as e:
        print(f"Processing error: {str(e)}")


# ===== EXAMPLE 5: Medication Reminder via Voice =====

def example_voice_medication_reminder():
    """
    Example: Add medication reminder using voice.
    """
    print("=== Example 5: Voice Medication Reminder ===\n")
    
    try:
        # Capture voice for medication name
        print("Say the medication name:")
        medicine_voice = listen_voice('english')
        
        print("Say the time (e.g., 'nine am' or '21:00'):")
        time_voice = listen_voice('english')
        
        print(f"\nMedicine: {medicine_voice}")
        print(f"Time: {time_voice}")
        print("(Would process this to extract medication name and time)")
        
    except Exception as e:
        print(f"Error: {str(e)}")


# ===== EXAMPLE 6: Error Handling =====

def example_error_handling():
    """
    Example showing proper error handling for voice input.
    """
    print("=== Example 6: Error Handling ===\n")
    
    # Example 1: Unsupported language
    try:
        text = listen_voice('spanish')  # Not supported
    except ValueError as e:
        print(f"Language error: {e}")
    
    # Example 2: Microphone not available
    try:
        text = listen_voice('english')  # Microphone needed
    except RuntimeError as e:
        print(f"Microphone error: {e}")
        print("Solution: Ensure microphone is connected and accessible")
    
    # Example 3: No speech detected
    try:
        text = listen_voice('english')  # Timeout if no speech
    except TimeoutError as e:
        print(f"Timeout: {e}")
        print("Solution: Ensure you spoke clearly within the timeout period")
    
    # Example 4: Speech not understood
    try:
        text = listen_voice('english')  # Unintelligible speech
    except Exception as e:
        print(f"Recognition error: {str(e)}")
        print("Solution: Speak more clearly or reduce background noise")


# ===== USAGE GUIDE =====

"""
VOICE ASSISTANT QUICK START:

1. Single Language (English):
   from voice_assistant import listen_voice
   text = listen_voice('english')
   
2. Single Language (Tamil):
   text = listen_voice('tamil')
   
3. User Selects Language:
   from voice_assistant import listen_voice_with_language_selection
   text, lang = listen_voice_with_language_selection()
   
4. Process Voice with Chatbot:
   from voice_assistant import listen_voice
   from chatbot import get_response
   
   user_text = listen_voice('english')
   bot_response = get_response(user_text)
   
5. From Audio File:
   from voice_assistant import recognize_from_audio_file
   text = recognize_from_audio_file('audio.wav', 'english')

SUPPORTED LANGUAGES:
- English (en-US)
- Tamil (ta-IN)

REQUIREMENTS:
- Microphone connected to computer
- SpeechRecognition library installed
- PyAudio installed
- Internet connection (for Google Speech API)
- Clear audio without excessive background noise
"""


if __name__ == "__main__":
    print("Voice Assistant Integration Examples")
    print("====================================\n")
    print("This file contains usage examples.")
    print("Import specific examples to use them.\n")
    print("Available examples:")
    print("  - example_english_voice_chat()")
    print("  - example_tamil_voice_chat()")
    print("  - example_voice_with_language_selection()")
    print("  - example_voice_from_audio_file()")
    print("  - example_voice_medication_reminder()")
    print("  - example_error_handling()")
