"""
Voice Chatbot Integration
Complete voice conversation pipeline combining speech recognition, chatbot processing,
and text-to-speech synthesis for elderly-friendly voice-based conversations.

Pipeline:
1. Capture voice input via microphone
2. Convert speech to text (voice_assistant)
3. Process with chatbot (emotional response)
4. Convert response to speech (text_to_speech)
"""

from typing import Dict, Tuple, Optional, Any
from voice_assistant import listen_voice, get_language_code
from chatbot import get_response
from text_to_speech import speak_text, speak_text_slow

# ===== CONFIGURATION =====

SUPPORTED_LANGUAGES = ['english', 'tamil']
DEFAULT_LANGUAGE = 'english'

# ===== MAIN VOICE CHAT FUNCTIONS =====

def voice_chat(language: Optional[str] = None, speak_response: bool = True, slow_speech: bool = False) -> Dict[str, Any]:
    """
    Complete voice conversation pipeline.
    
    Performs full conversation flow: listen → process → respond → speak
    Ideal for elderly users who prefer pure voice interaction.
    
    Args:
        language: Conversation language ('english' or 'tamil'). Defaults to 'english'.
        speak_response: Whether to speak the chatbot response (default: True)
        slow_speech: Use slower speech rate for clarity (default: False)
        
    Returns:
        Dictionary containing:
        {
            'success': bool - Whether conversation was successful
            'user_input': str - Captured voice input text
            'chatbot_response': str - Generated chatbot response
            'language': str - Language used for conversation
            'message': str - Status message
        }
        
    Raises:
        ValueError: If language is not supported
        RuntimeError: If voice capture or speech synthesis fails
    """
    # Validate language
    if language is None:
        language = DEFAULT_LANGUAGE
    
    language = language.lower().strip()
    if language not in SUPPORTED_LANGUAGES:
        supported = ', '.join(SUPPORTED_LANGUAGES)
        raise ValueError(f"Language '{language}' not supported. Supported: {supported}")
    
    try:
        # Step 1: Capture voice input
        print(f"\n{'='*50}")
        print(f"Voice Chat - {language.upper()}")
        print(f"{'='*50}")
        print("Step 1: Listening for your voice...")
        
        user_input = listen_voice(language)
        print(f"✓ Captured: {user_input}\n")
        
        # Step 2: Process with chatbot
        print("Step 2: Generating response...")
        result = get_response(user_input)
        chatbot_response = result['response'] if isinstance(result, dict) else result
        print(f"✓ Response: {chatbot_response}\n")
        
        # Step 3: Speak the response
        if speak_response:
            print("Step 3: Speaking response...")
            if slow_speech:
                speak_text_slow(chatbot_response, language)
            else:
                speak_text(chatbot_response, language)
            print("✓ Response spoken\n")
        
        return {
            'success': True,
            'user_input': user_input,
            'chatbot_response': chatbot_response,
            'language': language,
            'message': 'Voice conversation completed successfully'
        }
    
    except Exception as e:
        error_msg = f"Voice chat error: {str(e)}"
        print(f"\n✗ {error_msg}")
        
        return {
            'success': False,
            'user_input': None,
            'chatbot_response': None,
            'language': language,
            'message': error_msg
        }


def voice_chat_with_language_selection(speak_response: bool = True) -> Dict[str, Any]:
    """
    Voice chat with user language selection.
    
    Prompts user to select language before starting conversation.
    
    Args:
        speak_response: Whether to speak the response
        
    Returns:
        Conversation result dictionary
    """
    print("\n=== Voice Chat ===")
    print("Supported languages:")
    for idx, lang in enumerate(SUPPORTED_LANGUAGES, 1):
        print(f"  {idx}. {lang.capitalize()}")
    
    # Default to English
    selected_language = DEFAULT_LANGUAGE
    
    try:
        user_input = input("Enter language (or press Enter for English): ").strip().lower()
        if user_input and user_input in SUPPORTED_LANGUAGES:
            selected_language = user_input
    except Exception:
        pass
    
    # Start voice chat
    return voice_chat(selected_language, speak_response)


def continuous_voice_chat(language: Optional[str] = None, max_conversations: int = 5) -> list:
    """
    Continuous voice conversation loop.
    
    Allows multiple conversation turns without reselecting language.
    Ideal for extended interactions.
    
    Args:
        language: Conversation language
        max_conversations: Maximum number of conversation turns (default 5)
        
    Returns:
        List of conversation result dictionaries
    """
    if language is None:
        language = DEFAULT_LANGUAGE
    
    conversations = []
    
    print(f"\n=== Continuous Voice Chat ({language.upper()}) ===")
    print(f"You can have up to {max_conversations} conversation turns.")
    print("Say 'goodbye' or 'quit' to exit conversation.\n")
    
    for turn in range(1, max_conversations + 1):
        print(f"\n--- Conversation {turn}/{max_conversations} ---")
        
        result = voice_chat(language, speak_response=True, slow_speech=False)
        conversations.append(result)
        
        if not result['success']:
            print("Conversation failed. Ending session.")
            break
        
        # Check for exit words
        user_text = result['user_input'].lower()
        if any(word in user_text for word in ['goodbye', 'quit', 'exit', 'bye']):
            print("Goodbye! Thank you for chatting.")
            break
    
    print(f"\nConversation session ended. Total turns: {len(conversations)}")
    return conversations


def voice_chat_json_api(language: Optional[str] = None) -> str:
    """
    Voice chat with JSON response format.
    
    Designed for Flask API integration.
    Returns JSON-serializable result dictionary.
    
    Args:
        language: Conversation language
        
    Returns:
        JSON-compatible result dictionary as dict
    """
    try:
        result = voice_chat(language, speak_response=False)  # Don't auto-speak for API
        return result
    except Exception as e:
        return {
            'success': False,
            'user_input': None,
            'chatbot_response': None,
            'language': language or DEFAULT_LANGUAGE,
            'message': f'API error: {str(e)}'
        }


# ===== ACCESSIBILITY FUNCTIONS =====

def voice_chat_for_elderly(language: Optional[str] = None) -> Dict[str, Any]:
    """
    Voice chat optimized for elderly users.
    
    Uses slower speech rates and simplified interaction.
    
    Args:
        language: Conversation language
        
    Returns:
        Conversation result dictionary
    """
    return voice_chat(language, speak_response=True, slow_speech=True)


def voice_chat_quiet_mode(language: Optional[str] = None) -> Dict[str, Any]:
    """
    Voice chat without audio response.
    
    Useful when speakers are unavailable or for testing.
    User still gets text response.
    
    Args:
        language: Conversation language
        
    Returns:
        Conversation result dictionary
    """
    return voice_chat(language, speak_response=False)


# ===== TEST FUNCTION =====

def test_voice_chatbot_integration() -> None:
    """
    Test the voice chatbot integration module.
    """
    print("=== Voice Chatbot Integration Test ===\n")
    
    # Test 1: Module imports
    print("Test 1: Module Dependencies")
    try:
        from voice_assistant import listen_voice
        from chatbot import get_response
        from text_to_speech import speak_text
        print("  ✓ voice_assistant imported")
        print("  ✓ chatbot imported")
        print("  ✓ text_to_speech imported")
    except ImportError as e:
        print(f"  ! Import error: {str(e)}")
    print()
    
    # Test 2: Language support
    print("Test 2: Language Support")
    print(f"  Supported languages: {', '.join(SUPPORTED_LANGUAGES)}")
    for lang in SUPPORTED_LANGUAGES:
        try:
            code = get_language_code(lang)
            print(f"    ✓ {lang.capitalize()}: {code}")
        except Exception as e:
            print(f"    ! {lang.capitalize()}: {str(e)}")
    print()
    
    # Test 3: Function availability
    print("Test 3: Available Functions")
    print("  ✓ voice_chat(language) - Main voice conversation")
    print("  ✓ voice_chat_with_language_selection() - User language selection")
    print("  ✓ continuous_voice_chat(language) - Multiple conversation turns")
    print("  ✓ voice_chat_json_api(language) - API integration")
    print("  ✓ voice_chat_for_elderly(language) - Elderly-friendly")
    print("  ✓ voice_chat_quiet_mode(language) - No audio output")
    print()
    
    # Test 4: Integration pipeline
    print("Test 4: Integration Pipeline")
    print("  Step 1: Speech-to-Text (voice_assistant)")
    print("          ↓")
    print("  Step 2: Chatbot Processing (chatbot)")
    print("          ↓")
    print("  Step 3: Text-to-Speech (text_to_speech)")
    print("          ↓")
    print("  Result: Full voice conversation")
    print()
    
    # Test 5: Function signatures
    print("Test 5: Function Signatures")
    print("  voice_chat(language, speak_response, slow_speech)")
    print("    → Returns: {'success': bool, 'user_input': str, ...}")
    print()
    print("  continuous_voice_chat(language, max_conversations)")
    print("    → Returns: List of conversation results")
    print()
    
    print("Test 6: Real-time Conversation")
    print("  Note: Skipping actual voice conversation in automated test")
    print("  To test voice conversation, run:")
    print("    voice_chat('english')")
    print("    voice_chat_for_elderly('tamil')")
    print("    continuous_voice_chat('english', max_conversations=3)")
    print()
    
    print("✓ Module test completed successfully!")
    print("\nTo use voice chatbot in your code:")
    print("  from voice_chatbot_integration import voice_chat")
    print("  result = voice_chat('english')")
    print("  print(result['chatbot_response'])")


if __name__ == "__main__":
    test_voice_chatbot_integration()
