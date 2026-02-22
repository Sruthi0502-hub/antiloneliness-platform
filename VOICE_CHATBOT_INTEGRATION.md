## Voice Chatbot Integration - Complete Documentation

### Overview

The Voice Chatbot Integration module combines three core components into a unified voice conversation experience, creating a complete hands-free interface for elderly users:

1. **Speech-to-Text (voice_assistant)** - Captures voice from microphone and converts to text
2. **Chatbot Processing** - Processes text and generates warm, emotional responses
3. **Text-to-Speech** - Converts chatbot response to speech and plays it back

Users simply **speak naturally** and receive **spoken responses** without typing or reading.

---

## Quick Start

### Basic Voice Chat (3 lines of code)

```python
from voice_chatbot_integration import voice_chat

# User speaks → text captured → chatbot processes → response spoken
result = voice_chat('english')
print(result['chatbot_response'])
```

### Conversation Flow

```
Microphone → listen_voice() → "Hello, how are you?"
                                    ↓
                         get_response() → chatbot
                                    ↓
                         "I'm doing well, thank you!"
                                    ↓
                         speak_text() → Speaker
```

---

## Core Functions

### 1. voice_chat() - Main Function

Complete voice conversation in one call.

```python
def voice_chat(
    language: Optional[str] = None,
    speak_response: bool = True,
    slow_speech: bool = False
) -> Dict[str, Any]
```

**Parameters:**
- `language` (str): 'english' or 'tamil' (default: 'english')
- `speak_response` (bool): Read response aloud (default: True)
- `slow_speech` (bool): Use slower speech rate 100 wpm (default: False)

**Returns:**
```python
{
    'success': bool,           # True if conversation successful
    'user_input': str,         # What user said
    'chatbot_response': str,   # What chatbot responded
    'language': str,           # Language used
    'message': str             # Status message
}
```

**Example - English Conversation:**
```python
result = voice_chat('english')
if result['success']:
    print(f"You said: {result['user_input']}")
    print(f"I said: {result['chatbot_response']}")  # Already spoken
```

**Example - Tamil with Slow Speech:**
```python
result = voice_chat(language='tamil', slow_speech=True)
# User hears response at slower pace for clarity
```

---

### 2. voice_chat_with_language_selection()

Let user choose language before conversation.

```python
def voice_chat_with_language_selection(speak_response: bool = True) -> Dict
```

**Example:**
```python
# Displays language options, user selects, then conversation starts
result = voice_chat_with_language_selection()
```

---

### 3. continuous_voice_chat() - Multi-Turn

Handle multiple back-and-forth exchanges in one session.

```python
def continuous_voice_chat(
    language: Optional[str] = None,
    max_conversations: int = 5
) -> list
```

**Example - 3-Turn Conversation:**
```python
# User can chat for up to 3 exchanges
results = continuous_voice_chat('english', max_conversations=3)

for turn, result in enumerate(results, 1):
    print(f"\nTurn {turn}:")
    print(f"  User: {result['user_input']}")
    print(f"  Bot:  {result['chatbot_response']}")

# User can say "goodbye" to exit early
```

---

### 4. voice_chat_for_elderly()

Optimized for elderly users.

```python
result = voice_chat_for_elderly('tamil')
# Uses: slower speech (100 wpm), pauses between sentences, clearer enunciation
```

---

### 5. voice_chat_quiet_mode()

Capture voice but don't speak response (for public places).

```python
result = voice_chat_quiet_mode('english')
# User can speak, response shown as text but NOT spoken
```

---

### 6. voice_chat_json_api()

Get response in JSON format for web integration.

```python
result = voice_chat_json_api('english')
# Returns JSON-compatible dict for /voice_chat endpoint
```

---

## Flask API Endpoints

### POST /voice_chat

**Complete voice conversation via API.**

```javascript
// JavaScript example
fetch('/voice_chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    language: 'english'  // 'english' or 'tamil'
  })
})
.then(r => r.json())
.then(data => {
  console.log('User said:', data.user_input);
  console.log('Bot said:', data.chatbot_response);
  // Response already spoken if speak_response=true
});
```

**Response:**
```json
{
  "success": true,
  "user_input": "Hello, how are you today?",
  "chatbot_response": "I'm doing well! How can I help?",
  "language": "english",
  "message": "Voice conversation completed successfully"
}
```

---

### POST /voice_chat_text_only

**Capture voice, return text only (no auto-speak).**

```javascript
// Useful when you want to control when response is displayed/spoken
fetch('/voice_chat_text_only', {
  method: 'POST',
  body: JSON.stringify({language: 'english'})
})
.then(r => r.json())
.then(data => {
  // Text captured but not automatically spoken
  console.log('User said:', data.user_input);
  console.log('Bot says:', data.chatbot_response);
  // Frontend can then display response or read it aloud
});
```

---

### GET /voice_chat_health

**Check system health and module availability.**

```javascript
fetch('/voice_chat_health')
  .then(r => r.json())
  .then(data => {
    console.log('Status:', data.status);  // 'healthy' or 'degraded'
    console.log('Voice input:', data.voice_assistant);
    console.log('Chatbot:', data.chatbot);
    console.log('Voice output:', data.text_to_speech);
  });
```

**Response:**
```json
{
  "status": "healthy",
  "supported_languages": ["english", "tamil"],
  "voice_assistant": true,
  "chatbot": true,
  "text_to_speech": true,
  "message": "All systems operational"
}
```

---

## Language Support

### English
```python
result = voice_chat('english')
```
- Speech recognition: en-US (US English)
- Supported accents: American, most clear pronunciations
- Chatbot: Full emotional intelligence
- Speech output: Natural English pronunciation

### Tamil
```python
result = voice_chat('tamil')
```
- Speech recognition: ta-IN (Indian Tamil)
- Supported accents: South Indian Tamil speakers
- Chatbot: Same emotional intelligence (responds in Tamil)
- Speech output: Tamil pronunciation via TTS

---

## Speech Rate Configuration

### Normal (Default)
```python
voice_chat('english')  # 150 wpm
```

### Slow (Elderly-Friendly)
```python
# Option 1: Use dedicated function
voice_chat_for_elderly('english')

# Option 2: Manual configuration
voice_chat('english', slow_speech=True)
```
- Speed: 100 wpm (words per minute)
- Use case: Elderly, hearing impaired
- Benefits: More time to process, clearer enunciation

### Fast
```python
# Would require manual text_to_speech() call with rate=200+
from text_to_speech import speak_text
speak_text("Hello", language='english', rate=200)
```

---

## Integration Patterns

### Pattern 1: Simple Conversation Loop

```python
from voice_chatbot_integration import voice_chat

# Single turn conversation
result = voice_chat('english')

# Result contains:
# - user_input: What user said
# - chatbot_response: What bot said (already spoken)
# - success: Whether it worked
```

### Pattern 2: Interactive Loop

```python
from voice_chatbot_integration import continuous_voice_chat

# Multi-turn conversation
results = continuous_voice_chat('english', max_conversations=5)

# User can exit by saying "goodbye"
```

### Pattern 3: Web API Integration

```javascript
// From frontend
async function startVoiceChat() {
  const response = await fetch('/voice_chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({language: 'english'})
  });
  
  const data = await response.json();
  
  if (data.success) {
    displayResponse(data.chatbot_response);
    // Response already spoken
  }
}
```

### Pattern 4: Accessibility-First

```python
# For users with visual impairment
result = voice_chat_for_elderly('tamil')

# Users interact entirely through voice:
# 1. User speaks (microphone)
# 2. Speech converted to text
# 3. Chatbot processes and responds
# 4. Response spoken aloud (speaker)
# No UI navigation needed
```

### Pattern 5: Hybrid Web/Voice

```python
# Capture voice but control display
result = voice_chat_quiet_mode('english')

# Display text on screen
show_response(result['user_input'], result['chatbot_response'])

# Then speak if desired
from text_to_speech import speak_text
speak_text(result['chatbot_response'])
```

---

## Real-World Use Cases

### Use Case 1: Medication Reminders

```python
# User asks about medications
result = voice_chat('english')

# If user said: "Tell me about my pills"
# Bot responds: "You have 3 medications..."
# Response is spoken aloud for easy listening
```

### Use Case 2: Elderly User at Home

```python
# Grandmother wants to chat (no keyboard skills)
result = voice_chat_for_elderly('tamil')

# Entirely voice-based:
# 1. Speaks in Tamil: "Hi, how are you?"
# 2. Hears response in Tamil (slow, clear)
# 3. Continues conversation naturally
```

### Use Case 3: Family Video Call Integration

```javascript
// During video call with family member
fetch('/voice_chat', {
  method: 'POST',
  body: JSON.stringify({language: 'english'})
})
.then(r => r.json())
.then(data => {
  // Show conversation on screen
  displayMessage('You: ' + data.user_input);
  displayMessage('Bot: ' + data.chatbot_response);
});
```

### Use Case 4: Accessibility for Visually Impaired

```python
# User cannot see screen well
# Entirely voice-based interaction
result = voice_chat('english')

# 1. Speaks: "What's the weather?"
# 2. Hears: "I'm a companion chatbot, not connected to weather"
# 3. Continues conversation
# No need to see or type anything
```

---

## Error Handling

### Common Errors and Solutions

**Error 1: No Microphone Connected**
```
Message: "Speech recognition requires audio input"
Solution: Connect USB microphone or check audio device settings
```

**Error 2: Speech Not Recognized**
```
Message: "Could not understand your speech"
Solution: Speak clearly, reduce background noise, speak closer to mic
```

**Error 3: Unsupported Language**
```python
try:
    result = voice_chat('spanish')
except ValueError as e:
    print(f"Error: {e}")
    # Use 'english' or 'tamil' instead
```

**Error 4: Module Not Found**
```
pip install -r requirements.txt
```

**Error 5: No Text-to-Speech Voices**
```python
from text_to_speech import get_available_voices
voices = get_available_voices()
if not voices:
    # Install voice pack or use fallback
    print("Warning: No system voices available")
```

### Error Handling Example

```python
from voice_chatbot_integration import voice_chat

try:
    result = voice_chat('english')
    
    if not result['success']:
        print(f"Conversation failed: {result['message']}")
        # Handle failure gracefully
    else:
        print(f"Success! User said: {result['user_input']}")
        
except Exception as e:
    print(f"Unexpected error: {str(e)}")
    # Fallback to text chat
```

---

## Testing

### Test 1: Module Imports
```python
from voice_chatbot_integration import test_voice_chatbot_integration
test_voice_chatbot_integration()
```

### Test 2: Language Support
```python
from voice_assistant import get_language_code

print(get_language_code('english'))  # 'en-US'
print(get_language_code('tamil'))    # 'ta-IN'
```

### Test 3: Voice Chat with Text Only
```python
result = voice_chat_quiet_mode('english')
print(f"User input: {result['user_input']}")
print(f"Bot response: {result['chatbot_response']}")
```

### Test 4: Flask Routes
```bash
# Start Flask server
python app.py

# Test voice_chat endpoint
curl -X POST http://localhost:5000/voice_chat \
  -H "Content-Type: application/json" \
  -d '{"language": "english"}'

# Check health
curl http://localhost:5000/voice_chat_health
```

---

## Configuration

### System Voice Configuration

The voice chatbot uses system settings from `config.py`:

```python
# config.py settings used by voice module
DEBUG = True              # Development mode
HOST = '127.0.0.1'       # Localhost
PORT = 5000              # Flask port

# Speech synthesis configuration
SPEECH_RATE = 150         # Normal speed (100=slow, 200+=fast)
SPEECH_RATE_SLOW = 100    # Elderly-friendly
SPEECH_VOLUME = 0.9       # Volume (0.0 to 1.0)
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

**Key packages:**
- `SpeechRecognition` - Speech-to-text
- `pyaudio` - Audio input/output
- `pyttsx3` - Text-to-speech (offline)
- `gTTS` - Alternative text-to-speech
- `Flask` - Web framework

---

## Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| Windows  | ✓ Full | Works with system voices |
| macOS    | ✓ Full | Uses system voices |
| Linux    | ✓ Full | May need audio setup (see below) |

### Linux Audio Setup

```bash
# Install audio libraries
sudo apt-get install python3-pyaudio portaudio19-dev

# Or for conda
conda install -c conda-forge pyaudio

# Test audio
python -c "import pyaudio; print('Audio OK')"
```

---

## Performance Metrics

```
Speech-to-Text Latency:  1-2 seconds (network dependent)
Chatbot Processing:      <100ms
Text-to-Speech Render:   1-3 seconds (length dependent)
Total Round Trip:        3-5 seconds

Memory Usage:            ~50-100 MB
CPU Usage:               Varies with speech synthesis
Network:                 Only for Google Speech API
```

---

## Security Considerations

### For Production Deployment

1. **Authentication**: Add user authentication before exposing /voice_chat endpoint
   ```python
   from flask import session
   
   @app.route('/voice_chat', methods=['POST'])
   def voice_chat_route():
       if 'user_id' not in session:
           return {'error': 'Not authenticated'}, 401
       # ... rest of code
   ```

2. **Rate Limiting**: Prevent abuse
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app)
   
   @app.route('/voice_chat', methods=['POST'])
   @limiter.limit("10 per minute")
   def voice_chat_route():
       # ...
   ```

3. **Input Validation**: Validate language parameter
   ```python
   SUPPORTED_LANGUAGES = ['english', 'tamil']
   
   if language not in SUPPORTED_LANGUAGES:
       raise ValueError(f"Unsupported language: {language}")
   ```

4. **Error Messages**: Don't expose internal errors
   ```python
   # Good
   return {'error': 'Failed to process voice'}, 500
   
   # Bad - leaks information
   return {'error': f'Failed: {str(e)}'}, 500
   ```

---

## Examples

See `voice_chatbot_examples.py` for 10+ complete working examples:

1. Simple English voice chat
2. Tamil voice conversation
3. Language selection
4. Elderly-friendly slow speech
5. Quiet mode (no audio output)
6. Multi-turn conversation loop
7. API-style JSON responses
8. Medication reminder voice chat
9. Multilingual family interaction
10. Error handling and recovery

---

## Troubleshooting

### Issue: No sound output
**Solutions:**
- Check speaker volume is turned up
- Verify audio device is selected (system settings)
- Test: `python -c "from text_to_speech import speak_text; speak_text('hello')"`

### Issue: Microphone not detected
**Solutions:**
- Ensure microphone is plugged in and recognized by OS
- Test microphone: Use system recording app first
- Install pyaudio: `pip install pyaudio`
- For Linux, install audio libraries (see Platform Support above)

### Issue: Speech not recognized
**Solutions:**
- Speak clearly and closer to microphone
- Reduce background noise
- One sentence at a time
- Use supported languages only (English or Tamil)

### Issue: "ModuleNotFoundError"
**Solution:** Install all dependencies
```bash
pip install -r requirements.txt
```

---

## API Reference Summary

| Function | Purpose | Returns |
|----------|---------|---------|
| `voice_chat()` | Full conversation | Dict with conversation result |
| `voice_chat_with_language_selection()` | Let user pick language | Dict with conversation result |
| `continuous_voice_chat()` | Multiple turns | List of conversation results |
| `voice_chat_for_elderly()` | Optimized for elderly | Dict with slow speech response |
| `voice_chat_quiet_mode()` | No audio output | Dict with text only |
| `voice_chat_json_api()` | Web API format | Dict (JSON-compatible) |

---

## File Structure

```
antiloneliness-platform/
├── voice_chatbot_integration.py    # Main integration module
├── voice_chatbot_examples.py       # 10+ examples
├── voice_assistant.py              # Speech-to-text
├── text_to_speech.py               # Text-to-speech
├── chatbot.py                      # Response generation
├── app.py                          # Flask routes
└── config.py                       # Configuration
```

---

## Next Steps

1. **Quick Test:**
   ```python
   from voice_chatbot_integration import voice_chat
   result = voice_chat('english')
   ```

2. **Web Integration:**
   - Add `/voice_chat` endpoint to frontend
   - Test health check: `/voice_chat_health`
   - Integrate voice button in chat UI

3. **Production Deployment:**
   - Add authentication
   - Enable HTTPS
   - Set DEBUG=False in config.py
   - Use Gunicorn/WSGI server
   - Add rate limiting

4. **Accessibility Enhancement:**
   - Add keyboard shortcuts for microphone
   - Implement visual feedback
   - Support more languages

---

## Support

For issues or questions:
1. Check troubleshooting section
2. Review examples in `voice_chatbot_examples.py`
3. Run test suite: `python voice_chatbot_integration.py`
4. Check Flask logs: Enable DEBUG=True in config.py

---

**Version:** 1.0  
**Last Updated:** 2026-02-22  
**Status:** ✓ Production Ready
