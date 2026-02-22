# Sentimate - Combat Loneliness with Emotional Support

Sentimate is a web-based anti-loneliness platform designed specifically for elderly users. It combines AI-powered emotional support, health management tools, cognitive games, and activity monitoring to provide companionship and engagement, helping combat the psychological and physical effects of loneliness.

## 🎯 Features

### 1. **Emotional Support Chatbot**
- AI-powered conversational companion that responds with empathy and warmth
- Recognizes emotional cues and provides appropriate support
- 60+ unique responses across 9 response categories
- Keyword-based emotional intelligence for personalized conversations
- Error handling for offline and network issues

### 2. **Voice Assistant (Multi-lingual)**
- Native speech-to-text conversion for voice input
- Support for **Tamil** and **English** languages
- Real-time voice recognition with Google Speech API
- Seamless integration with chatbot for voice conversations
- Ideal for elderly users with typing difficulties
- Dynamic microphone adjustment for clear audio capture

### 3. **Text-to-Speech Output**
- Convert chatbot responses to natural speech
- Support for **English** and **Tamil** languages
- Offline speech synthesis using system TTS engine
- Configurable speech rate for clarity and accessibility
- Slow speech option ideal for elderly users
- Seamless integration with voice input for complete voice experience

### 4. **Medication Reminder Management**
- Create and manage medication reminder schedules
- Persistent storage with automatic recovery from data corruption
- Easy-to-use interface for adding/deleting reminders
- Reminders sorted by time for quick reference
- Input validation and user-friendly error messages

### 5. **Brain Games for Cognitive Engagement**
- Interactive 10-question quiz with multiple choice answers
- General knowledge questions to stimulate cognitive function
- Real-time scoring with encouraging feedback messages
- Inactivity detection alerts if user becomes inactive
- Responsive design optimized for accessibility

### 6. **Inactivity Detection & Alerts**
- Automatic monitoring of user activity
- 5-minute threshold for inactivity detection
- Real-time alerts when inactivity is detected
- Activity reset capability for quick dismissal of alerts
- Background monitoring with 60-second check intervals

## 🖥️ System Requirements

- **Python 3.x**
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- **Operating System**: Windows, macOS, or Linux

## 📋 Installation

### 1. Clone or Download the Repository
```bash
git clone <repository-url>
cd antiloneliness-platform
```

### 2. Create a Python Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

The application will start on `http://127.0.0.1:5000` in debug mode with automatic reloading.

## 🚀 Usage

### Home Page
Navigate to the home page to see all available features:
- **Chat** - Start a conversation with the emotional support chatbot
- **Medication** - Manage medication reminders
- **Brain Games** - Play the cognitive quiz

### Chat Page
1. Click on the "Chat" button from home
2. Type your message in the input field
3. The chatbot will respond with emotional support
4. Conversation history is displayed in the chat window

### Medication Reminders
1. Click on "Medication" from home
2. Enter medication name and time (HH:MM format)
3. Click "Add Reminder" to save
4. View all reminders in the list below
5. Click "Delete" to remove a reminder when taken

### Brain Games
1. Click on "Brain Games" from home
2. Answer 10 quiz questions by selecting an option
3. Submit your answers to see your score
4. Review feedback on your performance
5. Inactivity alerts will appear if you don't interact for 5 minutes

### Voice Assistant
1. **Enable voice input**: Use the microphone to speak instead of typing
2. **Supported languages**: Choose between English (en-US) and Tamil (ta-IN)
3. **Voice to text**: Speak naturally and the system converts speech to text
4. **Seamless integration**: Voice input works with the chatbot for real conversations
5. **Accessibility**: Perfect for users who prefer speaking or have difficulty typing

#### Voice Assistant Quick Guide
```python
from voice_assistant import listen_voice
from chatbot import get_response

# Capture English voice input
user_text = listen_voice('english')

# Get chatbot response
bot_response = get_response(user_text)
print(bot_response)
```

**Supported Languages:**
- English (en-US)
- Tamil (ta-IN)

**Requirements for Voice:**
- Microphone connected to computer
- Python packages: SpeechRecognition, pyaudio
- Internet connection (uses Google Speech API)
- Clear audio without excessive background noise

### Text-to-Speech Output
1. **Hear responses**: Chatbot responses are automatically spoken
2. **Supported languages**: English and Tamil speech output
3. **Configurable speed**: Control speech rate for comfort and understanding
4. **Offline operation**: Uses local system text-to-speech engine
5. **Accessibility**: Perfect for users with vision difficulties or preference for spoken content

#### Text-to-Speech Quick Guide
```python
from text_to_speech import speak_text, speak_text_slow
from chatbot import get_response

# Get chatbot response
response = get_response(user_input)

# Speak the response
speak_text(response, 'english')  # Normal speed

# Or speak slowly for important messages
speak_text_slow(response, 'english')  # Slower, clearer speech
```

**Supported Languages:**
- English (en-US)
- Tamil (ta-IN)

**Speech Rate Options:**
- Normal: 150 words per minute (default)
- Slow: 100 words per minute (elderly-friendly)
- Fast: 200+ words per minute (custom)

### Voice Chatbot Integration (Complete Voice Experience)
The Voice Chatbot Integration combines voice input, chatbot processing, and voice output into one seamless experience. Users can have natural, hands-free conversations entirely through voice.

**Complete Voice Conversation Pipeline:**
```
User speaks → listen_voice() → "Hello, how are you?"
                                        ↓
                               get_response() → chatbot
                                        ↓
                               "I'm doing well, thank you!"
                                        ↓
                               speak_text() → Speaker hears response
```

#### Voice Chatbot Quick Guide
```python
from voice_chatbot_integration import voice_chat

# Complete hands-free conversation in one call
result = voice_chat('english')

# User speaks → text captured → chatbot responds → response spoken
if result['success']:
    print(f"User said: {result['user_input']}")
    print(f"Bot said: {result['chatbot_response']}")  # Already spoken aloud
```

**Supported Languages:**
- English (en-US)
- Tamil (ta-IN)

**Available Functions:**
- `voice_chat()` - Single conversation turn
- `voice_chat_for_elderly()` - Slow speech (100 wpm) optimized for clarity
- `voice_chat_quiet_mode()` - Capture voice without audio output
- `continuous_voice_chat()` - Multiple conversation turns
- `voice_chat_with_language_selection()` - Let user choose language

**Web API Endpoints:**
- `POST /voice_chat` - Full voice conversation (returns result)
- `POST /voice_chat_text_only` - Voice input, text-only response
- `GET /voice_chat_health` - Check voice system health and supported languages

**Perfect For:**
- Elderly users who prefer speaking to typing
- Users with visual or motor impairments
- Hands-free interaction while cooking/exercising
- Multilingual families with different language preferences
- Building accessible voice-first interfaces

See `VOICE_CHATBOT_INTEGRATION.md` for complete documentation.

## 📁 Project Structure

```
antiloneliness-platform/
├── app.py                          # Flask application with all routes and endpoints
├── config.py                       # Centralized configuration settings
├── chatbot.py                      # Emotional support chatbot module
├── voice_assistant.py              # Voice input (Tamil & English) to text conversion
├── voice_assistant_examples.py     # Voice assistant usage examples
├── voice_chatbot_integration.py    # Complete voice conversation integration (NEW)
├── voice_chatbot_examples.py       # Voice chatbot integration examples (NEW)
├── text_to_speech.py               # Text-to-speech conversion (Tamil & English)
├── text_to_speech_examples.py      # Text-to-speech usage examples
├── medication_reminders.py         # Medication reminder management system
├── inactivity_detector.py         # User activity monitoring and inactivity detection
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── .gitignore                     # Git version control ignore patterns
├── VOICE_CHATBOT_INTEGRATION.md   # Complete voice integration documentation (NEW)
├── templates/                     # HTML templates
│   ├── home.html                 # Landing page with feature navigation
│   ├── chat.html                 # Chat companion interface
│   ├── medication.html           # Medication reminder management
│   ├── games.html                # Brain games quiz
│   └── navbar.html               # Reusable navigation component
├── static/                        # Static assets
│   └── css/
│       └── elderly-friendly.css  # Comprehensive styling for accessibility
└── data/                         # User data storage (created automatically)
    ├── reminders.json           # Medication reminders (JSON)
    └── activity.json            # User activity logs (JSON)
```

## ⚙️ Configuration

All application settings are centralized in `config.py`:

### Flask Settings
- `DEBUG`: Development mode toggle (default: True)
- `HOST`: Server host (default: 127.0.0.1)
- `PORT`: Server port (default: 5000)

### Inactivity Detection
- `INACTIVITY_THRESHOLD_MINUTES`: Time before inactivity alert (default: 5 minutes)
- `CHECK_INTERVAL_MS`: Activity check frequency (default: 60 seconds)

### Chatbot Configuration
- `ENABLE_EMOTIONAL_RESPONSES`: Toggle emotional responses (default: True)
- `MAX_MESSAGE_LENGTH`: Maximum message input length (default: 500 characters)

### Medication Settings
- `TIME_FORMAT`: Time input format (default: '%H:%M')
- `MAX_MEDICINE_NAME_LENGTH`: Maximum medicine name length (default: 100 characters)

### Games Configuration
- `QUIZ_QUESTION_COUNT`: Number of quiz questions (default: 10)

### Styling
The application includes predefined colors optimized for elderly users:
- Primary: Green (#4CAF50)
- Secondary: Gold (#FFB81C)
- Tertiary: Sage (#6B8E6F)
- Danger: Red (#D32F2F)
- Text: Dark Gray (#333333)
- Background: Off-White (#F5F5F5)

## 🔌 API Endpoints

### Voice Chatbot (Complete Voice Conversation)
- `POST /voice_chat` - Full voice conversation (listen → process → speak)
- `POST /voice_chat_text_only` - Voice input with text-only response  
- `GET /voice_chat_health` - Check voice system health and module availability

### Voice Assistant (Speech-to-Text Only)
- `POST /capture_voice` - Capture voice and convert to text (via voice_assistant module)

### Text-to-Speech (Speech Output Only)
- Routes handled via `text_to_speech` module (speak_text function)

### Activity Tracking
- `POST /update_activity` - Update user activity timestamp
- `GET /check_inactivity` - Check if user is inactive
- `GET /activity_status` - Get full activity status
- `POST /reset_inactivity` - Reset inactivity timer

### Medication Management
- `POST /add_reminder` - Create new medication reminder
- `GET /get_reminders` - Retrieve all reminders
- `DELETE /delete_reminder/<id>` - Delete a reminder by ID

### Chatbot
- `POST /get_response` - Get chatbot response for user message

### Page Routes
- `GET /` - Home page
- `GET /chat` - Chat page
- `GET /medication` - Medication reminder page
- `GET /reminder` - Alias for medication page
- `GET /games` - Brain games page

## 📊 Data Storage

The application uses JSON files for persistent data storage:

### reminders.json Structure
```json
[
  {
    "id": 1,
    "medicine_name": "Aspirin",
    "time": "09:00",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

### activity.json Structure
```json
{
  "last_activity": "2024-01-15T14:25:30",
  "user_id": null
}
```

## 🎨 Design Philosophy

The application follows elderly-friendly design principles:
- **Large Text**: Minimum 16px font size, scalable up to 40px
- **High Contrast**: Dark text on light backgrounds for readability
- **Simplified Navigation**: Clear button labels and minimal clutter
- **Responsive Design**: Works on desktop, tablet, and mobile browsers
- **Accessibility**: Focus states, reduced motion support, screen reader compatible
- **Warm Colors**: Encouraging use of greens and warm tones

## 🧪 Testing

### Running Tests
Each Python module includes a test function. To run them:

```bash
# Test chatbot
python -c "from chatbot import test_chatbot; test_chatbot()"

# Test medication reminders
python -c "from medication_reminders import test_reminder_system; test_reminder_system()"

# Test inactivity detection
python -c "from inactivity_detector import test_inactivity_system; test_inactivity_system()"

# Test voice assistant (speech-to-text)
python -c "from voice_assistant import test_voice_assistant; test_voice_assistant()"

# Test text-to-speech
python -c "from text_to_speech import test_text_to_speech; test_text_to_speech()"

# Test voice chatbot integration (speech-to-text + chatbot + speech output)
python -c "from voice_chatbot_integration import test_voice_chatbot_integration; test_voice_chatbot_integration()"
```

### Voice Chatbot Integration Testing
To test voice input in your application:

```python
from voice_assistant import listen_voice, listen_voice_with_language_selection

# Test English voice input
english_text = listen_voice('english')

# Test Tamil voice input
tamil_text = listen_voice('tamil')

# Test with language selection
text, language = listen_voice_with_language_selection()
```

### Text-to-Speech Testing
To test voice output in your application:

```python
from text_to_speech import speak_text, speak_text_slow, speak_multiple_sentences

# Test English speech
speak_text('Hello, how are you?', 'english')

# Test Tamil speech
speak_text('வணக்கம்', 'tamil')

# Test slow speech (ideal for important messages)
speak_text_slow('Please take your medicine now', 'english')

# Test multiple sentences
sentences = ['First sentence', 'Second sentence']
speak_multiple_sentences(sentences, 'english')
```

All test suites validate:
- Input validation
- Error handling
- Data persistence
- Response accuracy
- Edge cases
- Language support (English & Tamil)

## 🐛 Troubleshooting

### Application Won't Start
- Ensure Python 3.x is installed: `python --version`
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check that port 5000 is not in use

### Reminders Not Saving
- Ensure the `data/` directory exists (created automatically on first run)
- Check file permissions in the data directory
- Verify JSON files are not corrupted

### Chatbot Not Responding
- Check internet connection for live features
- Verify import statements in app.py are correct
- Review browser console for JavaScript errors

### Inactivity Detection Not Working
- Ensure JavaScript is enabled in browser
- Check that activity updates are being sent (browser Network tab)
- Verify config.py settings for threshold and intervals

### Voice Assistant Not Working
- **Microphone not detected**: Ensure microphone is connected and working
- **PyAudio installation fails**: This is a native extension; may require compilation tools
  - Windows: Install Visual C++ Build Tools
  - macOS: Install Xcode Command Line Tools
  - Linux: Install `python3-dev` and `portaudio19-dev`
- **No speech detected**: Speak clearly within the timeout period (default 10 seconds)
- **Speech not understood**: Reduce background noise and speak more clearly
- **Module import fails**: Verify SpeechRecognition is installed: `pip install SpeechRecognition==3.10.0`
- **API errors**: Check internet connection (uses Google Speech Recognition API)

### Text-to-Speech Not Working
- **No sound output**: Check system volume and speaker settings
- **Speech engine not found**: Ensure pyttsx3 is installed: `pip install pyttsx3==2.90`
- **Language not supported**: Currently only English and Tamil are supported
- **ModuleNotFoundError**: Run `pip install -r requirements.txt` to install all dependencies
- **No voices available**: Check system text-to-speech settings and install voices if needed
- **Sound issues on Linux**: Install `pulseaudio` or `alsa`: `sudo apt-get install pulseaudio`

## 🚀 Deployment

For production deployment:

1. Set `DEBUG = False` in `config.py`
2. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```
3. Consider using a reverse proxy like Nginx
4. Implement proper authentication and user sessions
5. Use a database instead of JSON files for production scale

## 📝 License

This project is created for the Antiloneliness initiative to help combat loneliness in elderly populations.

## 🤝 Contributing

Contributions are welcome. To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues, questions, or feature requests, please open an issue in the repository or contact the development team.

## 🎓 Acknowledgments

Sentimate is built with care for elderly users, combining modern web technologies with accessible design principles to create a warm, supportive digital companion.

---

**Last Updated**: January 2024  
**Version**: 1.0  
**Status**: Active Development
