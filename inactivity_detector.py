"""
Inactivity Detection System
Monitors user activity and triggers alerts when users are inactive for a set duration.
Helps ensure lonely elderly users receive timely check-ins from the app.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional

# ===== CONFIGURATION =====

# File path for persistent activity data
ACTIVITY_FILE = Path('data/activity.json')

# Threshold for inactivity alert (in minutes)
INACTIVITY_THRESHOLD = 5

# ===== UTILITY FUNCTIONS =====

def ensure_data_dir() -> None:
    """
    Create data directory if it doesn't exist.
    Called before any file operation to ensure directory is ready.
    """
    try:
        ACTIVITY_FILE.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Failed to create data directory: {str(e)}")

def load_activity_data() -> Dict[str, Any]:
    """
    Load activity data from JSON file with error handling.
    
    Returns:
        Activity data with 'last_activity' and 'user_id' keys
        
    Raises:
        RuntimeError: If file operation fails
    """
    ensure_data_dir()
    
    if not ACTIVITY_FILE.exists():
        return {'last_activity': None, 'user_id': None}
    
    try:
        with open(ACTIVITY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Ensure required keys exist
            if not isinstance(data, dict):
                return {'last_activity': None, 'user_id': None}
            return data
    except json.JSONDecodeError as e:
        print(f"Warning: Corrupted activity file, treating as empty: {str(e)}")
        return {'last_activity': None, 'user_id': None}
    except IOError as e:
        raise RuntimeError(f"Failed to read activity file: {str(e)}")

def save_activity_data(data: Dict[str, Any]) -> None:
    """
    Save activity data to JSON file with error handling.
    
    Args:
        data: Activity data to save
        
    Raises:
        RuntimeError: If file operation fails
    """
    if not isinstance(data, dict):
        raise ValueError("Activity data must be a dictionary")
    
    ensure_data_dir()
    
    try:
        with open(ACTIVITY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except IOError as e:
        raise RuntimeError(f"Failed to save activity file: {str(e)}")

# ===== MAIN ACTIVITY FUNCTIONS =====

def update_activity(user_id=None):
    """
    Update the last activity timestamp to current time.
    Called whenever user interacts with the app.
    
    Args:
        user_id (str, optional): User identifier for multi-user support
        
    Returns:
        dict: Updated activity data with timestamp
        
    Raises:
        RuntimeError: If file operation fails
    """
    try:
        activity_data = {
            'last_activity': datetime.now().isoformat(),
            'user_id': user_id,
            'timestamp': datetime.now().isoformat()
        }
        
        save_activity_data(activity_data)
        return activity_data
    except Exception as e:
        raise RuntimeError(f"Failed to update activity: {str(e)}")

def check_inactivity(user_id=None):
    """
    Check if user has been inactive for the threshold duration.
    Returns detailed information about inactivity status.
    
    Args:
        user_id (str, optional): User identifier (for future multi-user support)
        
    Returns:
        dict: Contains keys:
            - 'is_inactive' (bool): True if inactive threshold exceeded
            - 'message' (str): User-friendly message
            - 'minutes_inactive' (int): Minutes inactive (if is_inactive=True)
            - 'minutes_remaining' (int): Minutes until alert (if is_inactive=False)
            
    Raises:
        RuntimeError: If file operation fails
    """
    try:
        activity_data = load_activity_data()
        last_activity = activity_data.get('last_activity')
        
        # If no activity recorded yet, user just started
        if not last_activity:
            return {
                'is_inactive': False,
                'message': 'Activity tracking started.'
            }
        
        # Parse timestamp and calculate inactivity duration
        last_activity_time = datetime.fromisoformat(last_activity)
        current_time = datetime.now()
        inactivity_duration = current_time - last_activity_time
        
        # Check if inactivity threshold exceeded
        threshold_duration = timedelta(minutes=INACTIVITY_THRESHOLD)
        if inactivity_duration >= threshold_duration:
            minutes_inactive = int(inactivity_duration.total_seconds() / 60)
            return {
                'is_inactive': True,
                'message': f'You have been inactive for {minutes_inactive} minutes. Please take a moment to check in with yourself or continue using the app.',
                'minutes_inactive': minutes_inactive,
                'last_activity': last_activity
            }
        else:
            # User is still active
            minutes_remaining = INACTIVITY_THRESHOLD - int(inactivity_duration.total_seconds() / 60)
            return {
                'is_inactive': False,
                'message': f'User is active. Inactivity alert in {minutes_remaining} minutes.',
                'minutes_remaining': minutes_remaining
            }
    
    except ValueError as e:
        return {
            'is_inactive': False,
            'message': f'Unable to parse activity timestamp: {str(e)}'
        }
    except Exception as e:
        raise RuntimeError(f"Failed to check inactivity: {str(e)}")

def get_activity_status():
    """
    Get comprehensive activity status including inactivity check.
    
    Returns:
        dict: Complete activity status with:
            - 'last_activity': ISO format timestamp
            - 'is_inactive': Boolean flag
            - 'message': Status message
            - 'inactivity_threshold_minutes': Configured threshold
            
    Raises:
        RuntimeError: If file operation fails
    """
    try:
        activity_data = load_activity_data()
        inactivity_check = check_inactivity()
        
        return {
            'last_activity': activity_data.get('last_activity'),
            'is_inactive': inactivity_check['is_inactive'],
            'message': inactivity_check['message'],
            'inactivity_threshold_minutes': INACTIVITY_THRESHOLD
        }
    except Exception as e:
        raise RuntimeError(f"Failed to get activity status: {str(e)}")

def reset_inactivity():
    """
    Reset the inactivity timer by updating activity to current time.
    Called when user responds to inactivity alert.
    
    Returns:
        dict: Updated activity data
        
    Raises:
        RuntimeError: If file operation fails
    """
    return update_activity()

# ===== TEST SUITE =====

def test_inactivity_system():
    """
    Test the inactivity detection system with various scenarios.
    Verifies functionality and error handling.
    """
    import time
    
    print("=== Inactivity Detection System Test ===\n")
    
    # Test 1: Update activity
    print("Test 1: Updating activity...")
    try:
        result = update_activity(user_id='user123')
        print(f"  + Last activity: {result['last_activity']}")
    except Exception as e:
        print(f"  ! Error: {str(e)}")
    print()
    
    # Test 2: Check inactivity immediately (should be active)
    print("Test 2: Checking inactivity immediately...")
    try:
        status = check_inactivity()
        print(f"  + Is inactive: {status['is_inactive']}")
        print(f"  + Message: {status['message']}")
    except Exception as e:
        print(f"  ! Error: {str(e)}")
    print()
    
    # Test 3: Get full status
    print("Test 3: Getting full activity status...")
    try:
        activity_status = get_activity_status()
        print(f"  + Threshold: {activity_status['inactivity_threshold_minutes']} min")
        print(f"  + Is inactive: {activity_status['is_inactive']}")
    except Exception as e:
        print(f"  ! Error: {str(e)}")
    print()
    
    # Test 4: Simulate inactivity
    print("Test 4: Simulating 6 minutes of inactivity...")
    try:
        old_time = (datetime.now() - timedelta(minutes=6)).isoformat()
        activity_data = load_activity_data()
        activity_data['last_activity'] = old_time
        save_activity_data(activity_data)
        
        status = check_inactivity()
        print(f"  + Is inactive: {status['is_inactive']}")
        print(f"  + Minutes inactive: {status.get('minutes_inactive', 'N/A')}")
    except Exception as e:
        print(f"  ! Error: {str(e)}")
    print()
    
    # Test 5: Reset activity
    print("Test 5: Resetting inactivity...")
    try:
        reset_inactivity()
        status = check_inactivity()
        print(f"  + Is inactive: {status['is_inactive']}")
        print(f"  + Message: {status['message']}")
    except Exception as e:
        print(f"  ! Error: {str(e)}")
    print()
    
    print("=== Test Complete ===")

if __name__ == '__main__':
    test_inactivity_system()

def update_activity(user_id=None):
    """
    Update the last activity timestamp to current time.
    Called whenever user interacts with the app.
    
    Args:
        user_id (str, optional): User identifier for multi-user support
        
    Returns:
        dict: Updated activity data with timestamp
        
    Raises:
        RuntimeError: If file operation fails
    """
    try:
        activity_data = {
            'last_activity': datetime.now().isoformat(),
            'user_id': user_id,
            'timestamp': datetime.now().isoformat()
        }
        
        save_activity_data(activity_data)
        return activity_data
    except Exception as e:
        raise RuntimeError(f"Failed to update activity: {str(e)}")

def check_inactivity(user_id=None):
    """
    Check if user has been inactive for the threshold duration.
    Returns detailed information about inactivity status.
    
    Args:
        user_id (str, optional): User identifier (for future multi-user support)
        
    Returns:
        dict: Contains keys:
            - 'is_inactive' (bool): True if inactive threshold exceeded
            - 'message' (str): User-friendly message
            - 'minutes_inactive' (int): Minutes inactive (if is_inactive=True)
            - 'minutes_remaining' (int): Minutes until alert (if is_inactive=False)
            
    Raises:
        RuntimeError: If file operation fails
    """
    try:
        activity_data = load_activity_data()
        last_activity = activity_data.get('last_activity')
        
        # If no activity recorded yet, user just started
        if not last_activity:
            return {
                'is_inactive': False,
                'message': 'Activity tracking started.'
            }
        
        # Parse timestamp and calculate inactivity duration
        last_activity_time = datetime.fromisoformat(last_activity)
        current_time = datetime.now()
        inactivity_duration = current_time - last_activity_time
        
        # Check if inactivity threshold exceeded
        threshold_duration = timedelta(minutes=INACTIVITY_THRESHOLD)
        if inactivity_duration >= threshold_duration:
            minutes_inactive = int(inactivity_duration.total_seconds() / 60)
            return {
                'is_inactive': True,
                'message': f'You have been inactive for {minutes_inactive} minutes. Please take a moment to check in with yourself or continue using the app.',
                'minutes_inactive': minutes_inactive,
                'last_activity': last_activity
            }
        else:
            # User is still active
            minutes_remaining = INACTIVITY_THRESHOLD - int(inactivity_duration.total_seconds() / 60)
            return {
                'is_inactive': False,
                'message': f'User is active. Inactivity alert in {minutes_remaining} minutes.',
                'minutes_remaining': minutes_remaining
            }
    
    except ValueError as e:
        return {
            'is_inactive': False,
            'message': f'Unable to parse activity timestamp: {str(e)}'
        }
    except Exception as e:
        raise RuntimeError(f"Failed to check inactivity: {str(e)}")

def get_activity_status():
    """
    Get comprehensive activity status including inactivity check.
    
    Returns:
        dict: Complete activity status with:
            - 'last_activity': ISO format timestamp
            - 'is_inactive': Boolean flag
            - 'message': Status message
            - 'inactivity_threshold_minutes': Configured threshold
            
    Raises:
        RuntimeError: If file operation fails
    """
    try:
        activity_data = load_activity_data()
        inactivity_check = check_inactivity()
        
        return {
            'last_activity': activity_data.get('last_activity'),
            'is_inactive': inactivity_check['is_inactive'],
            'message': inactivity_check['message'],
            'inactivity_threshold_minutes': INACTIVITY_THRESHOLD
        }
    except Exception as e:
        raise RuntimeError(f"Failed to get activity status: {str(e)}")

def reset_inactivity():
    """
    Reset the inactivity timer by updating activity to current time.
    Called when user responds to inactivity alert.
    
    Returns:
        dict: Updated activity data
        
    Raises:
        RuntimeError: If file operation fails
    """
    return update_activity()


# ===== TEST SUITE =====

def test_inactivity_system():
    """
    Test the inactivity detection system with various scenarios.
    Verifies functionality and error handling.
    """
    import time
    
    print("=== Inactivity Detection System Test ===\n")
    
    # Test 1: Update activity
    print("Test 1: Updating activity...")
    try:
        result = update_activity(user_id='user123')
        print(f"  + Last activity: {result['last_activity']}")
    except Exception as e:
        print(f"  ! Error: {str(e)}")
    print()
    
    # Test 2: Check inactivity immediately (should be active)
    print("Test 2: Checking inactivity immediately...")
    try:
        status = check_inactivity()
        print(f"  + Is inactive: {status['is_inactive']}")
        print(f"  + Message: {status['message']}")
    except Exception as e:
        print(f"  ! Error: {str(e)}")
    print()
    
    # Test 3: Get full status
    print("Test 3: Getting full activity status...")
    try:
        activity_status = get_activity_status()
        print(f"  + Threshold: {activity_status['inactivity_threshold_minutes']} min")
        print(f"  + Is inactive: {activity_status['is_inactive']}")
    except Exception as e:
        print(f"  ! Error: {str(e)}")
    print()
    
    # Test 4: Simulate inactivity
    print("Test 4: Simulating 6 minutes of inactivity...")
    try:
        old_time = (datetime.now() - timedelta(minutes=6)).isoformat()
        activity_data = load_activity_data()
        activity_data['last_activity'] = old_time
        save_activity_data(activity_data)
        
        status = check_inactivity()
        print(f"  + Is inactive: {status['is_inactive']}")
        print(f"  + Minutes inactive: {status.get('minutes_inactive', 'N/A')}")
    except Exception as e:
        print(f"  ! Error: {str(e)}")
    print()
    
    # Test 5: Reset activity
    print("Test 5: Resetting inactivity...")
    try:
        reset_inactivity()
        status = check_inactivity()
        print(f"  + Is inactive: {status['is_inactive']}")
        print(f"  + Message: {status['message']}")
    except Exception as e:
        print(f"  ! Error: {str(e)}")
    print()
    
    print("=== Test Complete ===")

if __name__ == '__main__':
    test_inactivity_system()
