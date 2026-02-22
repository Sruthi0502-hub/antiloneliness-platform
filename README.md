# Sentimate - Combat Loneliness with Emotional Support

Sentimate is a web-based anti-loneliness platform designed specifically for elderly users. It combines AI-powered emotional support, health management tools, cognitive games, and activity monitoring to provide companionship and engagement, helping combat the psychological and physical effects of loneliness.

## 🎯 Features

### 1. **Emotional Support Chatbot**
- AI-powered conversational companion that responds with empathy and warmth
- Recognizes emotional cues and provides appropriate support
- 60+ unique responses across 9 response categories
- Keyword-based emotional intelligence for personalized conversations
- Error handling for offline and network issues

### 2. **Medication Reminder Management**
- Create and manage medication reminder schedules
- Persistent storage with automatic recovery from data corruption
- Easy-to-use interface for adding/deleting reminders
- Reminders sorted by time for quick reference
- Input validation and user-friendly error messages

### 3. **Brain Games for Cognitive Engagement**
- Interactive 10-question quiz with multiple choice answers
- General knowledge questions to stimulate cognitive function
- Real-time scoring with encouraging feedback messages
- Inactivity detection alerts if user becomes inactive
- Responsive design optimized for accessibility

### 4. **Inactivity Detection & Alerts**
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

## 📁 Project Structure

```
antiloneliness-platform/
├── app.py                          # Flask application with all routes and endpoints
├── config.py                       # Centralized configuration settings
├── chatbot.py                      # Emotional support chatbot module
├── medication_reminders.py         # Medication reminder management system
├── inactivity_detector.py         # User activity monitoring and inactivity detection
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── .gitignore                     # Git version control ignore patterns
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
```

All test suites validate:
- Input validation
- Error handling
- Data persistence
- Response accuracy
- Edge cases

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
