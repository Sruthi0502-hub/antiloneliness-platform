# -*- coding: utf-8 -*-
"""Quick import and sanity check for all modified modules."""
import sys, traceback

errors = []
mods = ['text_to_speech', 'chatbot', 'database', 'auth', 'voice_assistant', 'voice_chatbot_integration']
for m in mods:
    try:
        __import__(m)
        print(f'  OK  {m}')
    except Exception as e:
        print(f'  ERR {m}: {e}')
        errors.append(m)

print()

# Quick chatbot test: forced_language
from chatbot import get_response

r1 = get_response("Hello", username="test", forced_language="english")
assert r1['language'] == 'english', f"Expected english, got {r1['language']}"
assert 'response' in r1
print(f"  OK  forced english: {r1['response'][:60]}")

r2 = get_response("Hello", username="test", forced_language="tamil")
assert r2['language'] == 'tamil', f"Expected tamil, got {r2['language']}"
print(f"  OK  forced tamil:   {r2['response'][:60]}")

# Quick TTS test
from text_to_speech import speak_text, get_supported_languages, is_language_supported
assert is_language_supported('english')
assert is_language_supported('tamil')
langs = get_supported_languages()
assert 'english' in langs and 'tamil' in langs
print(f"  OK  text_to_speech: supported = {list(langs.keys())}")

# Quick DB test
from database import save_user_preference, get_user_preference
print("  OK  database helpers imported")

print()
print(f"RESULT: {'ALL OK' if not errors else 'FAILED: ' + str(errors)}")
