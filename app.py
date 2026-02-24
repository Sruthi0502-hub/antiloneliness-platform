"""
app.py – Sentimate
Flask application factory and route definitions.

Structure:
  [1] App setup & logging
  [2] Auth decorator
  [3] Auth routes         – /register  /login  /logout
  [4] Page routes         – /  /chat  /medication  /reminder  /dashboard
  [5] Games routes        – /games  /traditional_games  /pallanguli  /gilli
  [6] Activity endpoints  – /update_activity  /check_inactivity  /activity_status  /reset_inactivity
  [7] Reminder endpoints  – /add_reminder  /get_reminders  /delete_reminder/<id>
  [8] Chat endpoints      – /get_response  /get_history
  [9] Language endpoints  – /save_language  /get_language
  [10] Voice endpoints    – /speak_response  /voice_chat  /voice_chat_health
  [11] Error handlers     – 400  404  405  500
"""

import logging
import logging.handlers
import os
from functools import wraps

from flask import (
    Flask, render_template, request, jsonify,
    session, redirect, url_for, flash,
)

from chatbot import get_response
from medication_reminders import add_reminder, get_all_reminders, delete_reminder
from inactivity_detector import update_activity, check_inactivity, get_activity_status, reset_inactivity
from voice_chatbot_integration import voice_chat_json_api
from auth import register_user, authenticate_user
from database import (
    init_db, save_message, get_chat_history, get_recent_messages,
    save_user_preference, get_user_preference,
)
from helpers import api_err, parse_json_body, get_user_language, text_to_speech_b64, check_module
from config import DEBUG, HOST, PORT, SECRET_KEY, MAX_MESSAGE_LENGTH


# ── [1] App setup & logging ───────────────────────────────────────────────────

def _configure_logging() -> None:
    """Set up console + rotating-file logging for the application."""
    os.makedirs('logs', exist_ok=True)
    fmt = logging.Formatter(
        '[%(asctime)s] %(levelname)s %(name)s – %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    level = getattr(logging, os.environ.get('LOG_LEVEL', 'INFO').upper(), logging.INFO)

    console = logging.StreamHandler()
    console.setFormatter(fmt)

    file_handler = logging.handlers.RotatingFileHandler(
        'logs/sentimate.log', maxBytes=2_000_000, backupCount=3, encoding='utf-8'
    )
    file_handler.setFormatter(fmt)

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(console)
    root.addHandler(file_handler)


_configure_logging()
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config.update(
    JSON_SORT_KEYS=False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

init_db()


# ── [2] Auth decorator ────────────────────────────────────────────────────────

def login_required(f):
    """Redirect unauthenticated requests to the login page."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'info')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ── [3] Auth routes ───────────────────────────────────────────────────────────

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
        flash(message, 'success' if success else 'error')
        if success:
            return redirect(url_for('login'))

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
            session['user_id']  = user['id']
            session['username'] = user['username']
            flash(f"Welcome back, {user['username']}!", 'success')
            return redirect(url_for('home'))

        flash(message, 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Clear session and redirect to login."""
    username = session.get('username', 'unknown')
    session.clear()
    logger.info("User logged out: %s", username)
    flash('You have been logged out. See you soon!', 'info')
    return redirect(url_for('login'))


# ── [4] Page routes ───────────────────────────────────────────────────────────

@app.route('/')
@login_required
def home():
    return render_template('home.html')


@app.route('/chat')
@login_required
def chat():
    history = get_chat_history(session['user_id'], limit=50)
    return render_template('chat.html', history=history)


@app.route('/medication')
@login_required
def medication():
    return render_template('medication.html')


@app.route('/reminder')
@login_required
def reminder():
    """Backward-compat alias for /medication."""
    return redirect(url_for('medication'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


# ── [5] Games routes ──────────────────────────────────────────────────────────

@app.route('/games')
@login_required
def games():
    return render_template('games.html')


@app.route('/traditional_games')
@login_required
def traditional_games():
    return render_template('traditional_games.html')


@app.route('/pallanguli')
@login_required
def pallanguli():
    return render_template('pallanguli.html')


@app.route('/gilli')
@login_required
def gilli():
    return render_template('gilli.html')


# ── [6] Activity tracking endpoints ──────────────────────────────────────────

@app.route('/update_activity', methods=['POST'])
def update_activity_route():
    """Update the user's last-activity timestamp."""
    try:
        data    = request.get_json(silent=True) or {}
        user_id = data.get('user_id')
        result  = update_activity(user_id=user_id)
        return jsonify({'success': True, 'last_activity': result['last_activity']}), 200
    except Exception as exc:
        logger.error("update_activity failed: %s", exc)
        return api_err('Failed to update activity', 500)


@app.route('/check_inactivity', methods=['GET'])
def check_inactivity_route():
    """Return whether the user has been inactive beyond the threshold."""
    try:
        return jsonify(check_inactivity()), 200
    except Exception as exc:
        logger.error("check_inactivity failed: %s", exc)
        return api_err('Failed to check inactivity', 500)


@app.route('/activity_status', methods=['GET'])
def activity_status_route():
    """Return full activity status details."""
    try:
        return jsonify(get_activity_status()), 200
    except Exception as exc:
        logger.error("activity_status failed: %s", exc)
        return api_err('Failed to get activity status', 500)


@app.route('/reset_inactivity', methods=['POST'])
def reset_inactivity_route():
    """Reset the inactivity timer."""
    try:
        result = reset_inactivity()
        return jsonify({'success': True, 'last_activity': result['last_activity']}), 200
    except Exception as exc:
        logger.error("reset_inactivity failed: %s", exc)
        return api_err('Failed to reset inactivity', 500)


# ── [7] Reminder endpoints ────────────────────────────────────────────────────

@app.route('/add_reminder', methods=['POST'])
@login_required
def add_reminder_route():
    """Add a new medication reminder for the current user."""
    data, err = parse_json_body()
    if err:
        return err

    medicine_name = data.get('medicine_name', '').strip()
    time          = data.get('time', '').strip()

    if not medicine_name:
        return api_err('Medicine name is required')
    if not time:
        return api_err('Time is required')
    if len(medicine_name) > 100:
        return api_err('Medicine name is too long (max 100 characters)')

    try:
        reminder = add_reminder(medicine_name, time)
        return jsonify({'success': True, 'reminder': reminder}), 201
    except ValueError as exc:
        return api_err(str(exc), 400)
    except Exception as exc:
        logger.error("add_reminder failed: %s", exc)
        return api_err('Failed to save reminder', 500)


@app.route('/get_reminders', methods=['GET'])
@login_required
def get_reminders_route():
    """Return all medication reminders for the current user."""
    try:
        return jsonify({'reminders': get_all_reminders()}), 200
    except Exception as exc:
        logger.error("get_reminders failed: %s", exc)
        return api_err('Failed to retrieve reminders', 500)


@app.route('/delete_reminder/<int:reminder_id>', methods=['DELETE'])
@login_required
def delete_reminder_route(reminder_id: int):
    """Delete a reminder by ID (must belong to the current user)."""
    try:
        success = delete_reminder(reminder_id)
        if success:
            return jsonify({'success': True}), 200
        return api_err('Reminder not found', 404)
    except Exception as exc:
        logger.error("delete_reminder(%s) failed: %s", reminder_id, exc)
        return api_err('Failed to delete reminder', 500)


# ── [8] Chat endpoints ────────────────────────────────────────────────────────

@app.route('/get_response', methods=['POST'])
@login_required
def get_chatbot_response():
    """
    Get an AI chatbot response and persist both messages.
    Expects JSON: {"message": "..."}
    Returns JSON: {"response": str, "language": str}
    """
    data, err = parse_json_body()
    if err:
        return jsonify({'response': 'Please send a message.'}), 400

    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({'response': 'Please type a message!'}), 400
    if len(user_message) > MAX_MESSAGE_LENGTH:
        return jsonify({'response': 'Your message is too long. Please shorten it.'}), 400

    user_id      = session.get('user_id')
    username     = session.get('username', '')
    display_name = session.get('display_name')
    lang_pref    = get_user_language(user_id)

    # Fetch recent context for the chatbot
    recent_history = []
    if user_id:
        try:
            recent_history = get_recent_messages(user_id, limit=10)
        except Exception as exc:
            logger.warning("Could not load chat history for user %s: %s", user_id, exc)

    try:
        result = get_response(
            user_message,
            username=username,
            history=recent_history,
            display_name=display_name,
            forced_language=lang_pref,
        )
    except Exception as exc:
        logger.error("Chatbot get_response failed: %s", exc)
        return jsonify({'response': 'Sorry, I had trouble responding. Please try again.'}), 500

    bot_response  = result['response']
    language      = result.get('language', 'english')
    detected_name = result.get('detected_name')

    if detected_name:
        session['display_name'] = detected_name

    if user_id:
        try:
            save_message(user_id, 'user', user_message)
            save_message(user_id, 'bot', bot_response)
        except Exception as exc:
            logger.warning("Failed to save messages for user %s: %s", user_id, exc)

    return jsonify({'response': bot_response, 'language': language}), 200


@app.route('/get_history', methods=['GET'])
@login_required
def get_history_route():
    """
    Return chat history as JSON.
    Optional query param: ?limit=N  (1–200, default 50)
    """
    try:
        limit   = max(1, min(int(request.args.get('limit', 50)), 200))
        history = get_chat_history(session['user_id'], limit=limit)
        return jsonify({'history': history, 'count': len(history)}), 200
    except ValueError:
        return api_err("'limit' must be an integer", 400)
    except Exception as exc:
        logger.error("get_history failed: %s", exc)
        return api_err('Failed to load history', 500)


@app.route('/chat_history', methods=['GET'])
@login_required
def chat_history_route():
    """Backward-compat alias – delegates to /get_history."""
    return redirect(url_for('get_history_route', **request.args))


# ── [9] Language endpoints ────────────────────────────────────────────────────

_VALID_LANGUAGES = frozenset({'english', 'tamil'})


@app.route('/save_language', methods=['POST'])
@login_required
def save_language_route():
    """
    Persist the user's language preference.
    Expects JSON: {"language": "english"|"tamil"}
    """
    data, err = parse_json_body()
    if err:
        return err

    language = (data.get('language', 'english') or 'english').lower().strip()
    if language not in _VALID_LANGUAGES:
        return api_err(f'Invalid language. Supported: {", ".join(sorted(_VALID_LANGUAGES))}')

    user_id = session.get('user_id')
    try:
        if user_id:
            save_user_preference(user_id, 'language', language)
        session['lang_pref'] = language
        return jsonify({'success': True, 'language': language}), 200
    except Exception as exc:
        logger.error("save_language failed for user %s: %s", user_id, exc)
        return api_err('Failed to save language preference', 500)


@app.route('/get_language', methods=['GET'])
@login_required
def get_language_route():
    """Return the user's saved language preference."""
    lang = get_user_language(session.get('user_id'))
    return jsonify({'language': lang}), 200


# ── [10] Voice endpoints ──────────────────────────────────────────────────────

@app.route('/speak_response', methods=['POST'])
@login_required
def speak_response_route():
    """
    Convert text to speech. Returns base64-encoded MP3.
    Expects JSON: {"text": "...", "language": "english"|"tamil"}
    """
    data, err = parse_json_body()
    if err:
        return err

    text     = (data.get('text', '') or '').strip()
    language = (data.get('language', 'english') or 'english').lower()

    if not text:
        return api_err('No text provided')
    if len(text) > 1000:
        return api_err('Text is too long for TTS (max 1000 characters)')

    try:
        audio_b64 = text_to_speech_b64(text, language)
        return jsonify({'success': True, 'audio_b64': audio_b64}), 200
    except ImportError:
        logger.warning("gTTS not installed – TTS endpoint unavailable")
        return api_err('TTS library not installed on this server', 503)
    except Exception as exc:
        logger.error("speak_response failed: %s", exc)
        return api_err(f'TTS error: {exc}', 500)


@app.route('/voice_chat', methods=['POST'])
@login_required
def voice_chat_route():
    """Complete voice conversation (server-side mic capture)."""
    data     = (request.get_json(silent=True) or {})
    language = data.get('language', 'english').lower()

    try:
        result = voice_chat_json_api(language)
        status = 200 if result.get('success') else 400
        return jsonify(result), status
    except Exception as exc:
        logger.error("voice_chat failed: %s", exc)
        return jsonify({
            'success':          False,
            'user_input':       None,
            'chatbot_response': None,
            'language':         language,
            'message':          f'Voice chat error: {exc}',
        }), 500


@app.route('/voice_chat_health', methods=['GET'])
def voice_chat_health_route():
    """Health check for all voice-related modules."""
    voice_ok = check_module('voice_assistant', 'listen_voice')
    chat_ok  = check_module('chatbot', 'get_response')
    tts_ok   = check_module('text_to_speech', 'speak_text')

    all_ok = voice_ok and chat_ok and tts_ok
    return jsonify({
        'status':               'healthy' if all_ok else 'degraded',
        'supported_languages':  ['english', 'tamil'],
        'voice_assistant':      voice_ok,
        'chatbot':              chat_ok,
        'text_to_speech':       tts_ok,
        'message':              'All systems operational' if all_ok else 'Some modules unavailable',
    }), 200


# ── [11] Error handlers ───────────────────────────────────────────────────────

def _wants_json() -> bool:
    """True when the client prefers a JSON response (API call vs browser)."""
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' or request.path.startswith('/api/')


@app.errorhandler(400)
def bad_request(error):
    if _wants_json():
        return jsonify({'error': 'Bad request', 'code': 400}), 400
    return render_template('error.html', code=400, message='Bad Request'), 400


@app.errorhandler(404)
def page_not_found(error):
    if _wants_json():
        return jsonify({'error': 'Not found', 'code': 404}), 404
    return render_template('error.html', code=404, message='Page Not Found'), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed', 'code': 405}), 405


@app.errorhandler(500)
def internal_error(error):
    logger.exception("Unhandled 500 error: %s", error)
    if _wants_json():
        return jsonify({'error': 'Internal server error', 'code': 500}), 500
    return render_template('error.html', code=500, message='Internal Server Error'), 500


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
