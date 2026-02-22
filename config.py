"""
Configuration Module for Sentimate
Stores application settings and constants for easy management.
"""

import os
from pathlib import Path

# ===== APPLICATION SETTINGS =====

# Flask configuration
DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
HOST = os.environ.get('FLASK_HOST', '127.0.0.1')
PORT = int(os.environ.get('FLASK_PORT', 5000))

# ===== DATA STORAGE SETTINGS =====

# Base data directory
DATA_DIR = Path('data')

# File paths for persistent storage
REMINDERS_FILE = DATA_DIR / 'reminders.json'
ACTIVITY_FILE = DATA_DIR / 'activity.json'

# ===== INACTIVITY DETECTION =====

# Threshold for user inactivity alert (in minutes)
INACTIVITY_THRESHOLD_MINUTES = 5

# Interval to check inactivity (in milliseconds, frontend)
INACTIVITY_CHECK_INTERVAL_MS = 60000  # 60 seconds

# ===== CHATBOT SETTINGS =====

# Enable/disable chatbot emotional responses
ENABLE_EMOTIONAL_RESPONSES = True

# Max message length to accept (characters)
MAX_MESSAGE_LENGTH = 500

# ===== MEDICATION REMINDERS =====

# Valid time format
TIME_FORMAT = '%H:%M'  # HH:MM format (24-hour)

# Maximum length for medicine name
MAX_MEDICINE_NAME_LENGTH = 100

# ===== BRAIN GAMES =====

# Number of questions in quiz
QUIZ_QUESTION_COUNT = 10

# ===== LOGGING =====

# Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

# Log file path
LOG_FILE = 'logs/sentimate.log'

# Create logs directory if it doesn't exist
LOG_DIR = Path('logs')
LOG_DIR.mkdir(exist_ok=True)

# ===== ELDERLY-FRIENDLY SETTINGS =====

# Font size base (in em)
FONT_SIZE_BASE = 1.2  # 19.2px at 16px base

# Color scheme
COLORS = {
    'primary': '#6b8e6f',      # Green (chat)
    'secondary': '#d4a574',    # Gold (reminders)
    'tertiary': '#c8d4b8',     # Sage (games)
    'background': '#f5f3f0',   # Warm background
    'text': '#1a1a1a',         # Dark text
    'success': '#6b8e6f',      # Green
    'error': '#d9534f',        # Red
    'info': '#5bc0de',         # Blue
}

# ===== HELPER FUNCTIONS =====

def ensure_data_directory():
    """Create data directory if it doesn't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_environment():
    """Get current environment (development/production)."""
    return 'development' if DEBUG else 'production'


if __name__ == '__main__':
    print("=== Sentimate Configuration ===\n")
    print(f"Environment: {get_environment()}")
    print(f"Debug Mode: {DEBUG}")
    print(f"Host: {HOST}:{PORT}")
    print(f"Data Directory: {DATA_DIR.absolute()}")
    print(f"Inactivity Threshold: {INACTIVITY_THRESHOLD_MINUTES} minutes")
    print(f"Log Level: {LOG_LEVEL}")
