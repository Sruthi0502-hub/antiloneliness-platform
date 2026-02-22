"""
Text-to-Speech Integration Examples
Demonstrates how to use the text_to_speech module with Sentimate.
"""

from text_to_speech import (
    speak_text, 
    speak_text_slow,
    speak_chatbot_response,
    speak_multiple_sentences,
    get_available_voices
)
from chatbot import get_response
from voice_assistant import listen_voice

# ===== EXAMPLE 1: Simple English Text =====

def example_simple_english():
    """
    Simple example: Speak English text.
    """
    print("=== Example 1: Simple English Text ===\n")
    
    try:
        text = "Hello! This is a text-to-speech example."
        speak_text(text, 'english')
        print("Speech completed!\n")
    except Exception as e:
        print(f"Error: {str(e)}\n")


# ===== EXAMPLE 2: Tamil Text =====

def example_tamil_text():
    """
    Example speaking in Tamil language.
    """
    print("=== Example 2: Tamil Text ===\n")
    
    try:
        # Tamil greeting
        text = "வணக்கம்! உங்களுக்கு எப்படி இருக்கிறது?"
        speak_text(text, 'tamil')
        print("Tamil speech completed!\n")
    except Exception as e:
        print(f"Error: {str(e)}\n")


# ===== EXAMPLE 3: Voice Input + Chatbot + Speech Output =====

def example_voice_chat_with_speech():
    """
    Complete example: Voice input → Chatbot processing → Speech output
    This creates a fully voice-based conversation.
    """
    print("=== Example 3: Voice Chat with Speech Output ===\n")
    
    try:
        # Step 1: Get voice input
        print("Step 1: Listening for your voice input...")
        user_voice = listen_voice('english')
        print(f"You said: {user_voice}\n")
        
        # Step 2: Process through chatbot
        print("Step 2: Processing with chatbot...")
        bot_response = get_response(user_voice)
        print(f"Bot response: {bot_response}\n")
        
        # Step 3: Speak the response
        print("Step 3: Speaking response...")
        speak_chatbot_response(bot_response, 'english')
        print("Conversation complete!\n")
        
    except Exception as e:
        print(f"Error: {str(e)}\n")


# ===== EXAMPLE 4: Slow Speech for Elderly =====

def example_slow_elderly_friendly():
    """
    Example with slower speech rate, ideal for elderly users.
    """
    print("=== Example 4: Slow Speech (Elderly-Friendly) ===\n")
    
    try:
        important_message = (
            "This is an important medication reminder. "
            "Please take your medicine at 9 o'clock in the morning. "
            "Remember to drink water with your medicine."
        )
        
        print("Speaking at slow, clear pace...")
        speak_text_slow(important_message, 'english')
        print("Reminder spoken!\n")
        
    except Exception as e:
        print(f"Error: {str(e)}\n")


# ===== EXAMPLE 5: Multiple Sentences =====

def example_multiple_sentences():
    """
    Example speaking multiple sentences with pauses.
    """
    print("=== Example 5: Multiple Sentences ===\n")
    
    sentences = [
        "Good morning! How are you today?",
        "I hope you slept well.",
        "Would you like to have a conversation?",
        "Or perhaps play a game to exercise your mind?"
    ]
    
    try:
        print("Speaking multiple sentences with pauses...\n")
        speak_multiple_sentences(sentences, 'english')
        print("\nAll sentences spoken!\n")
    except Exception as e:
        print(f"Error: {str(e)}\n")


# ===== EXAMPLE 6: Medication Reminder with Voice =====

def example_medication_reminder_with_voice():
    """
    Example: Speak a medication reminder at scheduled time.
    """
    print("=== Example 6: Medication Reminder with Voice ===\n")
    
    medicine_name = "Aspirin"
    medicine_time = "9:00 AM"
    
    reminder_text = f"Reminder: It's time to take your {medicine_name} medication at {medicine_time}"
    
    try:
        speak_text_slow(reminder_text, 'english')
        print(f"Medication reminder spoken!\n")
    except Exception as e:
        print(f"Error: {str(e)}\n")


# ===== EXAMPLE 7: Multi-lingual Support =====

def example_multilingual():
    """
    Example showing English and Tamil support.
    """
    print("=== Example 7: Multi-lingual Support ===\n")
    
    conversations = [
        ("english", "Hello! How can I help you today?"),
        ("tamil", "வணக்கம்! நான் உங்களுக்கு எப்படி உதவ முடியும்?")
    ]
    
    try:
        for language, text in conversations:
            print(f"Speaking in {language.upper()}:")
            speak_text(text, language)
            print()
        
        print("Multi-lingual demo completed!\n")
    except Exception as e:
        print(f"Error: {str(e)}\n")


# ===== EXAMPLE 8: Available Voices =====

def example_check_available_voices():
    """
    Example showing how to check available voices on the system.
    """
    print("=== Example 8: Check Available Voices ===\n")
    
    try:
        voices = get_available_voices()
        
        print("Available English Voices:")
        if voices['english']:
            for idx, voice in enumerate(voices['english'], 1):
                print(f"  {idx}. {voice['name']}")
        else:
            print("  No English voices found")
        
        print("\nAvailable Tamil Voices:")
        if voices['tamil']:
            for idx, voice in enumerate(voices['tamil'], 1):
                print(f"  {idx}. {voice['name']}")
        else:
            print("  No Tamil voices found")
        
        print()
    except Exception as e:
        print(f"Error: {str(e)}\n")


# ===== EXAMPLE 9: Integration with Chatbot =====

def example_chatbot_integration():
    """
    Example integrating text-to-speech with chatbot for accessibility.
    """
    print("=== Example 9: Chatbot Integration ===\n")
    
    responses = [
        "Hello! It's so nice to hear from you.",
        "I'm here to listen and support you.",
        "Thank you for sharing that with me."
    ]
    
    try:
        print("Speaking chatbot responses...\n")
        for response in responses:
            print(f"Chatbot: {response}")
            speak_chatbot_response(response, 'english')
            print()
        
        print("Chatbot integration demo completed!\n")
    except Exception as e:
        print(f"Error: {str(e)}\n")


# ===== EXAMPLE 10: Error Handling =====

def example_error_handling():
    """
    Example showing proper error handling for text-to-speech.
    """
    print("=== Example 10: Error Handling ===\n")
    
    # Example 1: Empty text
    print("Test 1: Empty text")
    try:
        speak_text("", 'english')
    except ValueError as e:
        print(f"  Caught error: {e}\n")
    
    # Example 2: Unsupported language
    print("Test 2: Unsupported language")
    try:
        speak_text("Hello", 'spanish')
    except ValueError as e:
        print(f"  Caught error: {e}\n")
    
    # Example 3: Invalid text type
    print("Test 3: Invalid text type")
    try:
        speak_text(12345, 'english')
    except ValueError as e:
        print(f"  Caught error: {e}\n")
    
    print("Error handling examples completed!\n")


# ===== USAGE GUIDE =====

"""
TEXT-TO-SPEECH QUICK START:

1. Speak English Text:
   from text_to_speech import speak_text
   speak_text('Hello world!', 'english')
   
2. Speak Tamil Text:
   speak_text('வணக்கம்', 'tamil')
   
3. Speak at Slow Pace (Elderly-friendly):
   from text_to_speech import speak_text_slow
   speak_text_slow('Important message', 'english')
   
4. Multiple Sentences:
   from text_to_speech import speak_multiple_sentences
   sentences = ['First sentence', 'Second sentence']
   speak_multiple_sentences(sentences, 'english')
   
5. With Chatbot:
   from text_to_speech import speak_chatbot_response
   from chatbot import get_response
   
   bot_reply = get_response(user_input)
   speak_chatbot_response(bot_reply, 'english')

6. Check Available Voices:
   from text_to_speech import get_available_voices
   voices = get_available_voices()
   print(voices)

FEATURES:
- Offline speech synthesis (uses pyttsx3)
- English (en-US) and Tamil (ta-IN) support
- Configurable speech rate (50-300 wpm)
- Multiple voices available
- Elderly-friendly slow speech option
- Integration with voice input for full voice conversation

CONFIGURATION:
- Default rate: 150 wpm (slower than normal for clarity)
- Default volume: 0.9
- Slow rate: 100 wpm (for important information)
- Normal rate: 150 wpm
"""


if __name__ == "__main__":
    print("Text-to-Speech Integration Examples")
    print("===================================\n")
    print("Available examples:")
    print("  - example_simple_english()")
    print("  - example_tamil_text()")
    print("  - example_voice_chat_with_speech()")
    print("  - example_slow_elderly_friendly()")
    print("  - example_multiple_sentences()")
    print("  - example_medication_reminder_with_voice()")
    print("  - example_multilingual()")
    print("  - example_check_available_voices()")
    print("  - example_chatbot_integration()")
    print("  - example_error_handling()")
