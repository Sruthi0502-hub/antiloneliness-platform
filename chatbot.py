"""
Sentimate Chatbot Module
Provides warm, empathetic responses to elderly users.
Supports multiple conversation topics including greetings, emotional support,
health concerns, and family relationships.
"""

import random
from typing import Dict, List, Optional

# ===== RESPONSE LIBRARY =====
# Organized by conversation category for maintainability

RESPONSE_CATEGORIES = {
    # Warm greetings and welcome responses
    'greetings': [
        "Hello there! It's so nice to hear from you.",
        "Hello! I'm so glad you're here.",
        "Hi! How are you doing today?",
        "Hello! What a pleasure to chat with you.",
        "Hi there, friend! How can I help you today?",
        "Good to see you! How are you feeling?",
        "Hello! I'm always happy to talk with you.",
    ],
    
    # Status and well-being check-ins
    'status_check': [
        "I'm doing well, thank you for asking! How about you?",
        "I'm here and happy to chat with you. How's your day been?",
        "I'm doing great! Tell me, how are you feeling today?",
        "Wonderful! I'm so glad you asked. What's on your mind?",
        "I'm doing well, thanks for caring! How can I support you?",
        "I'm here for you. Is there something on your heart today?",
        "I'm doing wonderful! And you, my friend?",
    ],
    
    # Emotional support for loneliness and sadness
    'emotional_support': [
        "I can hear that you're feeling lonely. You're not alone - I'm here for you.",
        "It's okay to feel this way sometimes. Would you like to talk about it?",
        "Loneliness is difficult, but please know you're valued and cared for.",
        "I'm here to listen. Sometimes just sharing how we feel helps.",
        "You're important, and your feelings matter. I'm listening.",
        "Even on tough days, remember you have worth and purpose.",
        "It's brave to share your feelings. Let's talk through this together.",
    ],
    
    # Gratitude and appreciation responses
    'gratitude': [
        "You're very welcome! It's my pleasure to help.",
        "Thank you for your kind words! That means so much to me.",
        "I'm happy I could help. Thank you for talking with me.",
        "You're so kind to say that! I'm here whenever you need me.",
        "I appreciate your gratitude. Helping you brings me joy.",
        "Thank you! It's wonderful to be part of your day.",
        "You're welcome, my friend. I'm always here for you.",
    ],
    
    # Encouragement and positive affirmation
    'encouragement': [
        "You're doing great! Keep being your wonderful self.",
        "I believe in you! You have so much to offer.",
        "That's wonderful! You should be proud of yourself.",
        "What a great attitude! You inspire me.",
        "You're stronger than you know. Keep going!",
        "That's truly commendable. You're making a difference!",
        "I'm so proud of what you're doing. Keep up the good work!",
    ],
    
    # Memories and storytelling prompts
    'memories': [
        "I'd love to hear about your memories! Do you have a favorite story?",
        "Memories are such a treasure. What's something you remember fondly?",
        "You must have so many wonderful memories. Care to share one?",
        "Tell me about a happy moment from your life.",
        "What's a memory that always makes you smile?",
        "I love hearing about your past experiences. What comes to mind?",
        "Memories are precious. Would you like to share one with me?",
    ],
    
    # Health and wellness encouragement
    'health': [
        "Your health is so important! Are you taking good care of yourself?",
        "How's your health been? I hope you're feeling well.",
        "Remember to drink water and get some rest. Your wellbeing matters!",
        "Have you taken your medications today? Your health is crucial.",
        "I hope you're being kind to yourself and your body.",
        "Taking care of yourself shows self-love. That's wonderful!",
        "Your wellbeing is important to me. Are you doing okay?",
    ],
    
    # Conversation engagement and connection
    'conversation': [
        "I'd love to hear more about what you're thinking!",
        "Tell me more! I'm genuinely interested in what you have to say.",
        "That's interesting! What else is on your mind?",
        "I'm listening! Please, share more if you'd like.",
        "You have such interesting thoughts. Keep going!",
        "I love our conversations. What else would you like to talk about?",
        "Please continue! Your thoughts are valuable to me.",
    ],
    
    # Family and relationships
    'family': [
        "Family is so special. Do you have family members you'd like to talk about?",
        "Relationships with loved ones are precious. How's your family?",
        "Who is someone in your life that means a lot to you?",
        "Tell me about the people you love and care about.",
        "Family connections are wonderful. Is there someone special you'd like to tell me about?",
        "I'd love to hear about the people closest to your heart.",
        "Your loved ones are blessed to have you. How are your relationships?",
    ],
    
    # Default responses for unexpected input
    'default': [
        "That's an interesting thought! Tell me more about that.",
        "I appreciate what you're saying. How does that make you feel?",
        "That's something to think about! What else is on your mind?",
        "I'm here to listen whenever you need to talk.",
        "How can I help you feel better today?",
        "That sounds important to you. I'm here to support you.",
        "I understand. Is there something specific you'd like to discuss?",
        "You're doing well sharing your thoughts. Keep going!",
        "That's really interesting. Tell me more if you'd like.",
        "I'm here for you, no matter what you want to talk about.",
        "Thank you for sharing that with me. How are you feeling?",
        "I value every conversation we have. What else is on your heart?",
    ]
}

# ===== KEYWORD MAPPING =====
# Associates keywords with response categories

KEYWORD_TO_CATEGORY = {
    # Greeting keywords
    'hello': 'greetings',
    'hi': 'greetings',
    'hey': 'greetings',
    'greetings': 'greetings',
    
    # Status check keywords
    'how are you': 'status_check',
    'how are you doing': 'status_check',
    'how do you do': 'status_check',
    'how have you been': 'status_check',
    'what is your status': 'status_check',
    
    # Emotional support keywords
    'lonely': 'emotional_support',
    'loneliness': 'emotional_support',
    'sad': 'emotional_support',
    'sadness': 'emotional_support',
    'depressed': 'emotional_support',
    'depression': 'emotional_support',
    'unhappy': 'emotional_support',
    'upset': 'emotional_support',
    'worried': 'emotional_support',
    'anxiety': 'emotional_support',
    
    # Gratitude keywords
    'thank': 'gratitude',
    'thanks': 'gratitude',
    'appreciate': 'gratitude',
    'grateful': 'gratitude',
    
    # Encouragement keywords
    'accomplished': 'encouragement',
    'achievement': 'encouragement',
    'did something': 'encouragement',
    'proud': 'encouragement',
    'success': 'encouragement',
    
    # Memory keywords
    'remember': 'memories',
    'memory': 'memories',
    'remember when': 'memories',
    'long ago': 'memories',
    'the old days': 'memories',
    
    # Health keywords
    'health': 'health',
    'medicine': 'health',
    'medication': 'health',
    'doctor': 'health',
    'health care': 'health',
    'exercise': 'health',
    'eat': 'health',
    
    # Family keywords
    'family': 'family',
    'mother': 'family',
    'father': 'family',
    'children': 'family',
    'grandchild': 'family',
    'grandchildren': 'family',
    'spouse': 'family',
    'husband': 'family',
    'wife': 'family',
    'son': 'family',
    'daughter': 'family',
    'loved one': 'family',
}

# ===== MAIN CHATBOT FUNCTION =====

def get_response(user_message: str) -> str:
    """
    Generate a warm, empathetic chatbot response to user input.
    
    Args:
        user_message: The user's input message
        
    Returns:
        A warm and supportive response from the chatbot
        
    Raises:
        ValueError: If user_message is None or not a string
    """
    # Input validation
    if user_message is None:
        raise ValueError("Message cannot be None")
    
    if not isinstance(user_message, str):
        raise ValueError("Message must be a string")
    
    # Handle empty input
    message = user_message.strip()
    if not message:
        return "I'm here to listen. Feel free to share whatever's on your mind!"
    
    # Normalize input for keyword matching
    message_lower = message.lower()
    
    # Find matching category based on keywords
    category = _find_matching_category(message_lower)
    
    # Get response from appropriate category
    responses = RESPONSE_CATEGORIES.get(category, RESPONSE_CATEGORIES['default'])
    return random.choice(responses)


# ===== HELPER FUNCTIONS =====

def _find_matching_category(message_lower: str) -> str:
    """
    Find the best matching response category for a message.
    
    Args:
        message_lower: The user's message in lowercase
        
    Returns:
        The category name (default to 'default' if no match)
    """
    # Check multi-word keywords first (more specific)
    for keyword, category in sorted(KEYWORD_TO_CATEGORY.items(), 
                                    key=lambda x: len(x[0]), 
                                    reverse=True):
        if keyword in message_lower:
            return category
    
    # No keyword found, return default
    return 'default'


# ===== TEST FUNCTION =====

def test_chatbot() -> None:
    """
    Test the chatbot with sample inputs to verify functionality.
    """
    test_messages = [
        "Hello!",
        "How are you?",
        "I'm feeling lonely",
        "Thank you for listening",
        "I remember when I was young",
        "I'm happy today",
        "Tell me more",
        "I have grandchildren"
    ]
    
    print("=== Sentimate Chatbot Test ===\n")
    for message in test_messages:
        try:
            response = get_response(message)
            print(f"User: {message}")
            print(f"Bot: {response}\n")
        except Exception as e:
            print(f"Error with message '{message}': {str(e)}\n")


if __name__ == "__main__":
    test_chatbot()

