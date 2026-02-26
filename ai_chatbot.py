"""
Sentimate AI Chatbot Module
Provides intelligent AI-like responses
Acts as second brain for Sentimate
"""

import random


def get_ai_response(message, username=None):

    message = message.lower()

    # Emotional intelligence
    if "lonely" in message or "alone" in message:
        return random.choice([
            "I'm here with you. You never have to feel alone while talking to me.",
            "Sometimes talking helps reduce loneliness. Would you like to share more?",
            "You are not alone. I'm always here to listen."
        ])

    elif "sad" in message or "cry" in message:
        return random.choice([
            "I'm sorry you feel this way. Your feelings matter.",
            "It's okay to feel sad sometimes. I'm here with you.",
            "You can share anything with me safely."
        ])

    elif "happy" in message:
        return random.choice([
            "Your happiness makes me happy too.",
            "That's wonderful! Tell me more.",
            "It's nice to hear positive things from you."
        ])

    elif "family" in message:
        return random.choice([
            "Family memories are precious.",
            "Would you like to tell me about your family?",
            "Family brings warmth to life."
        ])

    elif "health" in message:
        return random.choice([
            "Health is very important.",
            "Did you take medicines today?",
            "Taking care of yourself matters."
        ])

    elif "name" in message:
        return "That is a nice name."

    else:
        return random.choice([
            "Tell me more.",
            "I am listening.",
            "Please continue.",
            "What else would you like to share?"
        ])