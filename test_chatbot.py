# -*- coding: utf-8 -*-
"""Quick verification test for chatbot v2."""
from chatbot import get_response

tests = [
    ("Hello!", "Meena", [], None),
    ("My name is Kamala", "testuser", [], None),
    ("I feel very lonely", "testuser", [], "Kamala"),
    ("\u0bb5\u0ba3\u0b95\u0bcd\u0b95\u0bae\u0bcd!", "testuser", [], None),
    ("\u0ba8\u0bbe\u0ba9\u0bcd \u0bae\u0bbf\u0b95\u0bb5\u0bc1\u0bae\u0bcd \u0ba4\u0ba9\u0bbf\u0bae\u0bc8\u0baf\u0bbe\u0b95 \u0b89\u0ba3\u0bb0\u0bcd\u0b95\u0bbf\u0bb1\u0bc7\u0ba9\u0bcd", "testuser", [], None),
    ("Thank you so much", "testuser", [
        {"sender": "user", "message": "I feel sad today"},
        {"sender": "bot",  "message": "I am here for you"},
    ], "Kamala"),
]

print("=== CHATBOT v2 TESTS ===\n")
passed = 0
for msg, user, hist, dn in tests:
    r = get_response(msg, username=user, history=hist, display_name=dn)
    assert isinstance(r, dict), "get_response must return dict"
    assert "response" in r,    "'response' key missing"
    assert "language" in r,    "'language' key missing"
    assert r["language"] in ("english", "tamil"), f"Unknown language: {r['language']}"
    print(f"[{r['language']:7}] IN : {msg}")
    print(f"          OUT: {r['response'][:90]}")
    if r.get("detected_name"):
        print(f"          NAME DETECTED: {r['detected_name']}")
    print()
    passed += 1

print(f"ALL {passed}/{len(tests)} TESTS PASSED")
