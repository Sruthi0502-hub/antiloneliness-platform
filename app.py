"""
Sentimate - Anti-Loneliness Platform
A web application designed to combat loneliness in elderly users through
chat, medication reminders, brain games, and activity monitoring.

Features:
- User authentication (register, login, logout)
- Emotional support through AI chatbot with voice input/output
- Medication reminder management (per-user, SQLite-backed)
- Brain games for cognitive engagement
- Inactivity detection with alerts
- Elderly-friendly interface design
"""

import base64
import io
from functools import wraps
from typing import Dict, Any, Tuple

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash

from chatbot import get_response
from medication_reminders import add_reminder, get_all_reminders, delete_reminder
from inactivity_detector import update_activity, check_inactivity, get_activity_status, reset_inactivity
from voice_chatbot_integration import voice_chat_json_api
from auth import register_user, authenticate_user
from database import init_db, save_message, get_chat_history
from config import DEBUG, HOST, PORT, SECRET_KEY

# ===== FLASK APP SETUP =====

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['JSON_SORT_KEYS'] = False

# Initialise database on startup
init_db()


# ===== AUTH DECORATOR =====

def login_required(f):
    """Redirect to login page if user is not authenticated."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'info')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ===== AUTH ROUTES =====

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page."""
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        success, message, user = register_user(username, password, confirm)

        if success:
            flash(message, 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'error')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        success, message, user = authenticate_user(username, password)

        if success:
            session['user_id']   = user['id']
            session['username']  = user['username']
            flash(f"Welcome back, {user['username']}!", 'success')
            return redirect(url_for('home'))
        else:
            flash(message, 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Clear session and redirect to login."""
    session.clear()
    flash('You have been logged out. See you soon!', 'info')
    return redirect(url_for('login'))


# ===== PAGE ROUTES (protected) =====

@app.route('/')
@login_required
def home() -> str:
    """Render the home page with navigation and feature buttons."""
    return render_template('home.html')


@app.route('/chat')
@login_required
def chat() -> str:
    """Render the chat companion page for conversations."""
    history = get_chat_history(session['user_id'], limit=50)
    return render_template('chat.html', history=history)


@app.route('/medication')
@login_required
def medication() -> str:
    """Render the medication reminder management page."""
    return render_template('medication.html')


@app.route('/reminder')
@login_required
def reminder() -> str:
    """Alias route for medication reminders for backward compatibility."""
    return render_template('medication.html')


@app.route('/games')
@login_required
def games() -> str:
    """Render the brain games page with quiz."""
    return render_template('games.html')


# ===== ACTIVITY TRACKING ENDPOINTS =====

@app.route('/update_activity', methods=['POST'])
def update_activity_route():
    """Update user activity timestamp to current time."""
    try:
        data = request.get_json()
        user_id = data.get('user_id') if data else None
        result = update_activity(user_id=user_id)
        return jsonify({'success': True, 'last_activity': result['last_activity']}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to update activity', 'details': str(e)}), 500

@app.route('/check_inactivity', methods=['GET'])
def check_inactivity_route():
    """Check if user has been inactive for the threshold time."""
    try:
        status = check_inactivity()
        return jsonify(status), 200
    except Exception as e:
        return jsonify({'error': 'Failed to check inactivity', 'details': str(e)}), 500

@app.route('/activity_status', methods=['GET'])
def activity_status_route():
    """Get full activity status including last activity time and inactivity check."""
    try:
        status = get_activity_status()
        return jsonify(status), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get activity status', 'details': str(e)}), 500

@app.route('/reset_inactivity', methods=['POST'])
def reset_inactivity_route():
    """Reset inactivity timer by updating activity to current time."""
    try:
        result = reset_inactivity()
        return jsonify({'success': True, 'last_activity': result['last_activity']}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to reset inactivity', 'details': str(e)}), 500


# ===== REMINDER MANAGEMENT ENDPOINTS =====

@app.route('/add_reminder', methods=['POST'])
@login_required
def add_reminder_route():
    """Add a new medication reminder."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        medicine_name = data.get('medicine_name', '').strip()
        time          = data.get('time', '').strip()

        if not medicine_name:
            return jsonify({'error': 'Medicine name is required'}), 400
        if not time:
            return jsonify({'error': 'Time is required'}), 400

        try:
            reminder = add_reminder(medicine_name, time)
            return jsonify({'success': True, 'reminder': reminder}), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    except Exception as e:
        return jsonify({'error': 'Failed to add reminder', 'details': str(e)}), 500

@app.route('/get_reminders', methods=['GET'])
@login_required
def get_reminders_route():
    """Retrieve all stored medication reminders, sorted by time."""
    try:
        reminders = get_all_reminders()
        return jsonify({'reminders': reminders}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve reminders', 'details': str(e)}), 500

@app.route('/delete_reminder/<int:reminder_id>', methods=['DELETE'])
@login_required
def delete_reminder_route(reminder_id):
    """Delete a medication reminder by ID."""
    try:
        success = delete_reminder(reminder_id)
        if success:
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'Reminder not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to delete reminder', 'details': str(e)}), 500


# ===== CHATBOT ENDPOINTS =====

@app.route('/get_response', methods=['POST'])
@login_required
def get_chatbot_response():
    """
    Get chatbot response from user message and persist both messages.

    Expects JSON: {"message": "..."}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'response': 'Please send a message'}), 400

        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify({'response': 'Please type a message!'}), 400

        # Get bot response
        bot_response = get_response(user_message)

        # Persist to chat history
        user_id = session.get('user_id')
        if user_id:
            try:
                save_message(user_id, 'user', user_message)
                save_message(user_id, 'bot', bot_response)
            except Exception:
                pass  # Don't fail the response if history save fails

        return jsonify({'response': bot_response}), 200

    except Exception as e:
        return jsonify({'response': 'Sorry, I had trouble responding. Please try again.'}), 500


# ===== VOICE CHATBOT ENDPOINTS =====

@app.route('/speak_response', methods=['POST'])
@login_required
def speak_response_route():
    """
    Convert text to speech using gTTS and return base64-encoded MP3.

    Expects JSON: {"text": "...", "language": "english"|"tamil"}
    Returns JSON: {"audio_b64": "...", "success": true}
    """
    try:
        from gtts import gTTS

        data     = request.get_json()
        text     = (data.get('text', '') if data else '').strip()
        language = (data.get('language', 'english') if data else 'english').lower()

        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400

        lang_code = 'ta' if language == 'tamil' else 'en'

        tts = gTTS(text=text, lang=lang_code, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        audio_b64 = base64.b64encode(audio_buffer.read()).decode('utf-8')

        return jsonify({'success': True, 'audio_b64': audio_b64}), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/voice_chat', methods=['POST'])
@login_required
def voice_chat_route():
    """Complete voice conversation endpoint (server-side mic capture)."""
    try:
        data     = request.get_json()
        language = data.get('language', 'english').lower() if data else 'english'
        result   = voice_chat_json_api(language)

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({
            'success': False, 'user_input': None,
            'chatbot_response': None, 'language': 'english',
            'message': f'Voice chat error: {str(e)}'
        }), 500


@app.route('/voice_chat_health', methods=['GET'])
def voice_chat_health_route():
    """Check voice chat system health."""
    try:
        try:
            from voice_assistant import listen_voice
            voice_assistant_ok = True
        except ImportError:
            voice_assistant_ok = False

        try:
            from chatbot import get_response as _gr
            chatbot_ok = True
        except ImportError:
            chatbot_ok = False

        try:
            from text_to_speech import speak_text
            text_to_speech_ok = True
        except ImportError:
            text_to_speech_ok = False

        all_ok = voice_assistant_ok and chatbot_ok and text_to_speech_ok
        return jsonify({
            'status': 'healthy' if all_ok else 'degraded',
            'supported_languages': ['english', 'tamil'],
            'voice_assistant': voice_assistant_ok,
            'chatbot': chatbot_ok,
            'text_to_speech': text_to_speech_ok,
            'message': 'All systems operational' if all_ok else 'Some modules unavailable'
        }), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ===== CHAT HISTORY ENDPOINT =====

@app.route('/chat_history', methods=['GET'])
@login_required
def chat_history_route():
    """Return the current user's chat history as JSON."""
    try:
        history = get_chat_history(session['user_id'], limit=100)
        return jsonify({'history': history}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===== ERROR HANDLERS =====

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 Not Found errors."""
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server Error."""
    return jsonify({'error': 'Internal server error'}), 500


# ===== APPLICATION ENTRY POINT =====

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
