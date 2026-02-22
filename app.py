"""
Sentimate - Anti-Loneliness Platform
A web application designed to combat loneliness in elderly users through
chat, medication reminders, brain games, and activity monitoring.

Features:
- Emotional support through AI chatbot
- Medication reminder management
- Brain games for cognitive engagement
- Inactivity detection with alerts
- Elderly-friendly interface design
"""

from typing import Dict, Any, Tuple
from flask import Flask, render_template, request, jsonify
from chatbot import get_response
from medication_reminders import add_reminder, get_all_reminders, delete_reminder
from inactivity_detector import update_activity, check_inactivity, get_activity_status, reset_inactivity
from config import DEBUG, HOST, PORT

# Initialize Flask application
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# ===== PAGE ROUTES =====

@app.route('/')
def home() -> str:
    """Render the home page with navigation and feature buttons."""
    return render_template('home.html')


@app.route('/chat')
def chat() -> str:
    """Render the chat companion page for conversations."""
    return render_template('chat.html')


@app.route('/medication')
def medication() -> str:
    """Render the medication reminder management page."""
    return render_template('medication.html')


@app.route('/reminder')
def reminder() -> str:
    """Alias route for medication reminders for backward compatibility."""
    return render_template('medication.html')


@app.route('/games')
def games() -> str:
    """Render the brain games page with quiz."""
    return render_template('games.html')

# ===== ACTIVITY TRACKING ENDPOINTS =====

@app.route('/update_activity', methods=['POST'])
def update_activity_route():
    """
    Update user activity timestamp to current time.
    
    Expects JSON payload:
    {
        "user_id": "optional_user_identifier"
    }
    """
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
def add_reminder_route():
    """
    Add a new medication reminder.
    
    Expects JSON payload:
    {
        "medicine_name": "Name of medication",
        "time": "HH:MM format time"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        medicine_name = data.get('medicine_name', '').strip()
        time = data.get('time', '').strip()
        
        # Validate required fields
        if not medicine_name:
            return jsonify({'error': 'Medicine name is required'}), 400
        
        if not time:
            return jsonify({'error': 'Time is required'}), 400
        
        # Attempt to add reminder
        try:
            reminder = add_reminder(medicine_name, time)
            return jsonify({'success': True, 'reminder': reminder}), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
            
    except Exception as e:
        return jsonify({'error': 'Failed to add reminder', 'details': str(e)}), 500

@app.route('/get_reminders', methods=['GET'])
def get_reminders_route():
    """Retrieve all stored medication reminders, sorted by time."""
    try:
        reminders = get_all_reminders()
        return jsonify({'reminders': reminders}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve reminders', 'details': str(e)}), 500

@app.route('/delete_reminder/<int:reminder_id>', methods=['DELETE'])
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
def get_chatbot_response():
    """
    Get chatbot response from user message.
    
    Expects JSON payload:
    {
        "message": "User's chat message"
    }
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
        return jsonify({'response': bot_response}), 200
        
    except Exception as e:
        return jsonify({'response': 'Sorry, I had trouble responding. Please try again.'}), 500

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


