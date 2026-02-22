import random

def get_response(user_message):
    """
    Get a friendly and supportive response from the chatbot.
    
    Args:
        user_message (str): The user's message
        
    Returns:
        str: The bot's response
    """
    
    user_message = user_message.lower().strip()
    
    # Hello/Greeting responses
    if any(word in user_message for word in ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']):
        greetings = [
            "Hello! It's so nice to hear from you! How are you doing today?",
            "Hi there! I'm so glad you're here. What's on your mind?",
            "Hey! Welcome back! How can I help you today?",
            "Hello! It's wonderful to connect with you. Tell me, how are you feeling?",
            "Hi! I'm here to listen and chat with you. What would you like to talk about?"
        ]
        return random.choice(greetings)
    
    # How are you responses
    if any(phrase in user_message for phrase in ['how are you', 'how do you do', 'how are you doing', 'how\'s it going']):
        responses = [
            "I'm doing well, thank you for asking! That's very kind of you. More importantly, how are *you* doing?",
            "I'm great! I appreciate you asking. It makes me happy to hear from you. How are you feeling today?",
            "I'm doing wonderfully, and I'm so happy you asked! I'm here and ready to listen to you. How can I support you?",
            "Thank you for asking! I'm here and happy to chat with you. How are things going in your world?",
            "I'm doing well! It's really kind of you to ask. Tell me, how are you doing? I'm all ears!"
        ]
        return random.choice(responses)
    
    # Feeling lonely responses
    if any(phrase in user_message for phrase in ['lonely', 'alone', 'isolated', 'bad mood', 'sad', 'down', 'depressed', 'missing people']):
        responses = [
            "I hear you, and I want you to know that you're not truly alone. I'm here for you right now. Tell me, what's making you feel this way?",
            "It's completely okay to feel lonely sometimes. The fact that you're sharing this with me means a lot. I'm here to listen and support you. What would help you feel better?",
            "I can understand how that feels, and I'm so glad you felt comfortable sharing with me. You deserve companionship and support. Let's talk about it.",
            "Loneliness is a real feeling, and you're brave for acknowledging it. Remember, you have me to talk to anytime. What's been on your heart?",
            "I'm sorry you're feeling this way, but I want you to know you're not alone right now. I'm here with you. Tell me what you need?"
        ]
        return random.choice(responses)
    
    # Thank you responses
    if any(word in user_message for word in ['thank', 'thanks', 'appreciate', 'grateful', 'thank you']):
        responses = [
            "You're very welcome! It's my pleasure to be here for you. That's what I'm here for!",
            "Aw, thank you for that! It makes me happy to help. Is there anything else you'd like to talk about?",
            "You're so kind! I'm grateful to be able to chat with you too. Feel free to come back anytime you need to talk.",
            "My pleasure! That's really sweet of you to say. I'm always here whenever you need someone to talk to.",
            "Thank *you* for reaching out! It means so much to connect with you. Is there anything else on your mind?"
        ]
        return random.choice(responses)
    
    # Default/Unknown responses
    default_responses = [
        "That's interesting! Tell me more about that. I'd love to hear what you're thinking.",
        "I see! I'm here to listen and support you. How does that make you feel?",
        "That sounds important to you. Can you tell me a bit more about it?",
        "I'm really interested in what you're saying. What else would you like to share?",
        "Thank you for telling me that. Is there anything else you'd like to talk about?",
        "I understand. I'm here for you, no matter what you need to discuss.",
        "That's great! I'm glad you shared that with me. What would you like to talk about next?",
        "I'm listening! Please, tell me more. Your thoughts and feelings matter.",
    ]
    return random.choice(default_responses)


# Test the chatbot
if __name__ == "__main__":
    test_messages = [
        "Hello!",
        "How are you?",
        "I'm feeling lonely",
        "Thank you for listening",
        "What's the meaning of life?"
    ]
    
    print("=== Chatbot Test ===\n")
    for message in test_messages:
        response = get_response(message)
        print(f"User: {message}")
        print(f"Bot: {response}\n")
