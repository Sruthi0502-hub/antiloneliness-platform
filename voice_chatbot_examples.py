"""
Voice Chatbot Integration Examples
Complete working examples of voice-based conversations using the integrated
voice assistant, chatbot, and text-to-speech modules.

These examples demonstrate the full voice conversation pipeline:
microphone input → speech-to-text → chatbot processing → text-to-speech output
"""

from voice_chatbot_integration import (
    voice_chat,
    voice_chat_with_language_selection,
    continuous_voice_chat,
    voice_chat_for_elderly,
    voice_chat_quiet_mode,
    voice_chat_json_api
)

# ===== EXAMPLE 1: SIMPLE ENGLISH CONVERSATION =====

def example_simple_english_voice_chat() -> None:
    """
    Example 1: Basic voice conversation in English
    
    User speaks English → converted to text → processing → response is spoken
    Ideal for quick voice interactions.
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Simple English Voice Conversation")
    print("="*60)
    print("\nInstructions: Speak clearly after you see 'Listening...'")
    print("The bot will respond and speak the answer.\n")
    
    result = voice_chat(language='english', speak_response=True)
    
    print("\nResult:")
    print(f"  Success: {result['success']}")
    if result['success']:
        print(f"  You said: {result['user_input']}")
        print(f"  Bot said: {result['chatbot_response']}")
    else:
        print(f"  Error: {result['message']}")


# ===== EXAMPLE 2: TAMIL VOICE CONVERSATION =====

def example_tamil_voice_chat() -> None:
    """
    Example 2: Voice conversation in Tamil
    
    Demonstrates Tamil language support for elderly users
    who prefer their mother tongue.
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Tamil Voice Conversation")
    print("="*60)
    print("\nNotes: பேசு - Speak clearly in Tamil after listening prompt")
    print("The response will be spoken in Tamil.\n")
    
    result = voice_chat(language='tamil', speak_response=True)
    
    print("\nResult:")
    print(f"  Success: {result['success']}")
    if result['success']:
        print(f"  You said (Tamil): {result['user_input']}")
        print(f"  Bot said (Tamil): {result['chatbot_response']}")
    else:
        print(f"  Error: {result['message']}")


# ===== EXAMPLE 3: VOICE CHAT WITH LANGUAGE SELECTION =====

def example_voice_chat_with_language_selection() -> None:
    """
    Example 3: Let user choose language interactively
    
    Presents language options to user before conversation
    Useful for multi-lingual support.
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: Voice Chat with Language Selection")
    print("="*60 + "\n")
    
    result = voice_chat_with_language_selection(speak_response=True)
    
    print("\nConversation Summary:")
    print(f"  Language: {result['language']}")
    print(f"  User said: {result['user_input']}")
    print(f"  Bot said: {result['chatbot_response']}")


# ===== EXAMPLE 4: ELDERLY-FRIENDLY SLOW SPEECH =====

def example_elderly_friendly_voice_chat() -> None:
    """
    Example 4: Voice chat optimized for elderly users
    
    Uses slower speech rate (100 wpm) for clarity
    Ideal for users with hearing or comprehension needs
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: Elderly-Friendly Voice Chat")
    print("="*60)
    print("\nFeatures: Slower speech rate (100 wpm) for clarity\n")
    
    # voice_chat_for_elderly uses slow_speech=True
    result = voice_chat_for_elderly(language='english')
    
    if result['success']:
        print(f"User input: {result['user_input']}")
        print(f"Bot response (spoken slowly): {result['chatbot_response']}")
        print("\nNote: Response was spoken at slow speed for clarity")
    else:
        print(f"Error: {result['message']}")


# ===== EXAMPLE 5: QUIET MODE (NO AUDIO OUTPUT) =====

def example_quiet_mode_voice_chat() -> None:
    """
    Example 5: Voice capture without audio response
    
    Listens for user voice but doesn't speak response
    Suitable for public spaces or situations without speakers
    """
    print("\n" + "="*60)
    print("EXAMPLE 5: Quiet Mode Voice Chat")
    print("="*60)
    print("\nFeatures: Captures speech, displays text response only\n")
    
    # voice_chat_quiet_mode doesn't speak the response
    result = voice_chat_quiet_mode(language='english')
    
    if result['success']:
        print(f"You said: {result['user_input']}")
        print(f"\nBot response (text only, not spoken):")
        print(f"  {result['chatbot_response']}")
    else:
        print(f"Error: {result['message']}")


# ===== EXAMPLE 6: CONTINUOUS CONVERSATION (MULTI-TURN) =====

def example_continuous_voice_chat() -> None:
    """
    Example 6: Multi-turn conversation session
    
    Allows multiple back-and-forth exchanges without
    resetting language between turns.
    
    Say "goodbye" or "quit" to end the conversation.
    """
    print("\n" + "="*60)
    print("EXAMPLE 6: Continuous Multi-Turn Voice Chat")
    print("="*60)
    print("\nNote: You can have up to 3 conversation turns")
    print("Say 'goodbye' or 'quit' to end early\n")
    
    # Start continuous conversation with max 3 turns
    conversations = continuous_voice_chat(language='english', max_conversations=3)
    
    print("\n" + "-"*60)
    print("Conversation Summary:")
    print("-"*60)
    for idx, conv in enumerate(conversations, 1):
        if conv['success']:
            print(f"\nTurn {idx}:")
            print(f"  You: {conv['user_input']}")
            print(f"  Bot: {conv['chatbot_response']}")
    
    print(f"\nTotal conversation turns: {len([c for c in conversations if c['success']])}")


# ===== EXAMPLE 7: API-STYLE VOICE CHAT =====

def example_api_style_voice_chat() -> None:
    """
    Example 7: Voice chat with JSON API response
    
    Demonstrates the voice chat in a format suitable
    for web API integration and frontend communication.
    """
    print("\n" + "="*60)
    print("EXAMPLE 7: API-Style Voice Chat Response")
    print("="*60 + "\n")
    
    # Use API function that returns JSON-compatible dict
    result = voice_chat_json_api(language='english')
    
    print("API Response (JSON format):")
    print(f"  {result}\n")
    
    print("Usage in web frontend:")
    print("  fetch('/voice_chat', {")
    print("    method: 'POST',")
    print("    headers: {'Content-Type': 'application/json'},")
    print("    body: JSON.stringify({language: 'english'})")
    print("  }).then(r => r.json())")
    print("    .then(data => {")
    print("      console.log('User said:', data.user_input);")
    print("      console.log('Bot said:', data.chatbot_response);")
    print("    });")


# ===== EXAMPLE 8: MEDICATION REMINDER WITH VOICE =====

def example_medication_reminder_with_voice() -> None:
    """
    Example 8: Voice chat for medication reminders
    
    User can ask about medications and get voice responses
    about their medication reminders.
    """
    print("\n" + "="*60)
    print("EXAMPLE 8: Medication Reminder with Voice")
    print("="*60)
    print("\nScenario: User asks about their medication")
    print("Try saying things like:")
    print("  - 'What medications do I need to take?'")
    print("  - 'Tell me about my pills'")
    print("  - 'When do I take medicine?'\n")
    
    result = voice_chat(language='english', speak_response=True)
    
    if result['success']:
        print(f"\nUser asked: {result['user_input']}")
        print(f"Bot response: {result['chatbot_response']}")
        print("\nNote: Response was spoken aloud for easy listening")
    else:
        print(f"Error: {result['message']}")


# ===== EXAMPLE 9: MULTILINGUAL FAMILY SYSTEM =====

def example_multilingual_family_interaction() -> None:
    """
    Example 9: Multi-turn conversation with language flexibility
    
    Shows how different family members could interact
    using their preferred languages with voice.
    """
    print("\n" + "="*60)
    print("EXAMPLE 9: Multilingual Family Voice Chat")
    print("="*60)
    print("\nScenario: Elderly grandmother prefers Tamil,")
    print("now having first conversation...\n")
    
    # Grandmother speaks Tamil
    print("Grandmother's turn (Tamil):")
    result_tamil = voice_chat(language='tamil', speak_response=True)
    
    if result_tamil['success']:
        print(f"  Grandmother: {result_tamil['user_input']}")
        print(f"  Bot (Tamil): {result_tamil['chatbot_response']}\n")
    
    # Family member would speak English (example)
    print("English speaker interaction:")
    print("  (Would follow similar pattern with language='english')")
    
    print("\nMulti-lingual Support:")
    print("  ✓ Tamil (ta-IN) - For elderly users")
    print("  ✓ English (en-US) - For family members")


# ===== EXAMPLE 10: ERROR HANDLING AND RECOVERY =====

def example_error_handling_voice_chat() -> None:
    """
    Example 10: Handling voice chat errors gracefully
    
    Demonstrates error handling for common issues:
    - No microphone connected
    - Speech not recognized
    - Invalid language
    - API errors
    """
    print("\n" + "="*60)
    print("EXAMPLE 10: Error Handling in Voice Chat")
    print("="*60 + "\n")
    
    # Test with invalid language
    print("Test 1: Invalid language request")
    try:
        result = voice_chat(language='spanish')
        print(f"  Result: {result['message']}")
    except ValueError as e:
        print(f"  ✗ Caught error: {str(e)}")
    
    print()
    
    # Test with valid language
    print("Test 2: Valid language (English)")
    try:
        result = voice_chat(language='english', speak_response=False)
        if result['success']:
            print(f"  ✓ Success: Captured speech")
        else:
            print(f"  ! Issue: {result['message']}")
            print("    (This is normal if no microphone is available)")
    except Exception as e:
        print(f"  ! Error: {str(e)}")
    
    print("\nCommon Issues and Solutions:")
    print("  • No microphone: Check hardware connectivity")
    print("  • Speech not recognized: Speak clearly, reduce background noise")
    print("  • Unsupported language: Use 'english' or 'tamil'")
    print("  • Module not found: pip install -r requirements.txt")


# ===== HOME PAGE ACCESSIBILITY EXAMPLE =====

def example_voice_chat_accessibility() -> None:
    """
    Example: Voice chat for accessibility
    
    Shows how to integrate voice chat for users with:
    - Visual impairment (can't read well)
    - Motor control issues (can't type)
    - Cognitive challenges (prefer spoken interaction)
    """
    print("\n" + "="*60)
    print("ACCESSIBILITY: Voice Chat for All Users")
    print("="*60 + "\n")
    
    print("Use Cases:")
    print("  1. Visually impaired users")
    print("     → Speak naturally, hear chatbot response")
    print("\n  2. Physically limited users")
    print("     → No need for keyboard/mouse, just speak")
    print("\n  3. Elderly users")
    print("     → Slow speech, large fonts, warm colors")
    print("\n  4. Non-native speakers")
    print("     → Support for Tamil and other languages")
    
    print("\n" + "-"*60)
    print("Example Usage:")
    print("  result = voice_chat('english')")
    print("  # User speaks: 'Hello, how are you?'")
    print("  # Bot responds: 'I'm here to help!'")
    print("  # Response is spoken aloud for user to hear")
    print("-"*60)


# ===== MAIN EXECUTION =====

if __name__ == "__main__":
    print("\n" + "="*60)
    print("VOICE CHATBOT INTEGRATION EXAMPLES")
    print("="*60)
    print("\nAvailable Examples:")
    print("  1. example_simple_english_voice_chat()")
    print("  2. example_tamil_voice_chat()")
    print("  3. example_voice_chat_with_language_selection()")
    print("  4. example_elderly_friendly_voice_chat()")
    print("  5. example_quiet_mode_voice_chat()")
    print("  6. example_continuous_voice_chat()")
    print("  7. example_api_style_voice_chat()")
    print("  8. example_medication_reminder_with_voice()")
    print("  9. example_multilingual_family_interaction()")
    print("  10. example_error_handling_voice_chat()")
    print("  11. example_voice_chat_accessibility()")
    
    print("\n" + "="*60)
    print("To run an example, import and call the function:")
    print("  from voice_chatbot_examples import example_simple_english_voice_chat")
    print("  example_simple_english_voice_chat()")
    print("="*60 + "\n")
    
    # Uncomment to run a specific example:
    # example_simple_english_voice_chat()
    # example_voice_chat_with_language_selection()
    # example_continuous_voice_chat()
    # example_error_handling_voice_chat()
