"""
Medication Reminder System
Manages user medication reminders with persistent JSON storage.
Provides functions to add, retrieve, and delete medication reminders.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# ===== CONFIGURATION =====

# File path for persistent storage of reminders
REMINDERS_FILE = Path('data/reminders.json')

# ===== UTILITY FUNCTIONS =====

def ensure_data_dir() -> None:
    """
    Create data directory if it doesn't exist.
    Called before any file operation to ensure directory is ready.
    """
    try:
        REMINDERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Failed to create data directory: {str(e)}")

def load_reminders() -> List[Dict[str, Any]]:
    """
    Load reminders from JSON file with error handling.
    
    Returns:
        List of reminder dictionaries, or empty list if file doesn't exist
        
    Raises:
        RuntimeError: If file operation fails
    """
    ensure_data_dir()
    
    if not REMINDERS_FILE.exists():
        return []
    
    try:
        with open(REMINDERS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Ensure we always return a list
            return data if isinstance(data, list) else []
    except json.JSONDecodeError as e:
        print(f"Warning: Corrupted reminders file, treating as empty: {str(e)}")
        return []
    except IOError as e:
        raise RuntimeError(f"Failed to read reminders file: {str(e)}")

def save_reminders(reminders: List[Dict[str, Any]]) -> None:
    """
    Save reminders to JSON file with error handling.
    
    Args:
        reminders: List of reminder dictionaries to save
        
    Raises:
        RuntimeError: If file operation fails
    """
    if not isinstance(reminders, list):
        raise ValueError("Reminders must be a list")
    
    ensure_data_dir()
    
    try:
        with open(REMINDERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(reminders, f, indent=2, ensure_ascii=False)
    except IOError as e:
        raise RuntimeError(f"Failed to save reminders file: {str(e)}")


# ===== MAIN REMINDER FUNCTIONS =====

def add_reminder(medicine_name: str, time: str, user_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Add a new medication reminder with full validation.
    
    Args:
        medicine_name: Name of the medication
        time: Time in HH:MM (24-hour) format
        user_id: User identifier for multi-user support
        
    Returns:
        The created reminder with ID and timestamp
        
    Raises:
        ValueError: If inputs are invalid (empty medicine name, invalid time format)
        RuntimeError: If file operation fails
    """
    # Validate medicine name
    if medicine_name is None:
        raise ValueError("Medicine name cannot be None")
    
    medicine_name_clean = str(medicine_name).strip()
    if not medicine_name_clean:
        raise ValueError("Medicine name cannot be empty")
    
    # Validate time
    if time is None:
        raise ValueError("Time cannot be None")
    
    time_clean = str(time).strip()
    if not time_clean:
        raise ValueError("Time cannot be empty")
    
    # Validate time format (HH:MM)
    try:
        datetime.strptime(time_clean, '%H:%M')
    except ValueError:
        raise ValueError("Time must be in HH:MM format (e.g., 08:30, 14:45)")
    
    # Load existing reminders
    reminders = load_reminders()
    
    # Generate unique ID based on current count
    reminder_id = max([r.get('id', 0) for r in reminders] + [0]) + 1
    
    # Create reminder object
    reminder = {
        'id': reminder_id,
        'medicine_name': medicine_name_clean,
        'time': time_clean,
        'created_at': datetime.now().isoformat(),
        'user_id': user_id
    }
    
    # Save and return
    reminders.append(reminder)
    save_reminders(reminders)
    
    return reminder

def get_all_reminders(user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieve all medication reminders, optionally filtered by user.
    
    Args:
        user_id: If provided, only return reminders for this user
        
    Returns:
        List of reminders sorted by time (ascending)
        
    Raises:
        RuntimeError: If file operation fails
    """
    try:
        reminders = load_reminders()
        
        # Filter by user if specified
        if user_id:
            reminders = [r for r in reminders if r.get('user_id') == user_id]
        
        # Sort by time (HH:MM format sorts correctly alphabetically)
        reminders.sort(key=lambda x: x.get('time', '00:00'))
        
        return reminders
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve reminders: {str(e)}")

def delete_reminder(reminder_id: int) -> bool:
    """
    Delete a reminder by its ID.
    
    Args:
        reminder_id: The ID of the reminder to delete
        
    Returns:
        True if reminder was deleted, False if not found
        
    Raises:
        ValueError: If reminder_id is not a valid integer
        RuntimeError: If file operation fails
    """
    try:
        if not isinstance(reminder_id, int):
            reminder_id = int(reminder_id)
    except (ValueError, TypeError):
        raise ValueError("Reminder ID must be an integer")
    
    try:
        reminders = load_reminders()
        original_count = len(reminders)
        
        # Filter out the reminder to delete
        reminders = [r for r in reminders if r.get('id') != reminder_id]
        
        # Check if anything was deleted
        if len(reminders) < original_count:
            save_reminders(reminders)
            return True
        
        return False
    except Exception as e:
        raise RuntimeError(f"Failed to delete reminder: {str(e)}")

def clear_all_reminders(user_id: Optional[str] = None) -> None:
    """
    Clear all reminders, optionally for a specific user only.
    
    Args:
        user_id: If provided, only clear reminders for this user
        
    Raises:
        RuntimeError: If file operation fails
    """
    try:
        reminders = load_reminders()
        
        if user_id:
            # Keep reminders for other users
            reminders = [r for r in reminders if r.get('user_id') != user_id]
        else:
            # Clear all
            reminders = []
        
        save_reminders(reminders)
    except Exception as e:
        raise RuntimeError(f"Failed to clear reminders: {str(e)}")

# ===== TEST SUITE =====

def test_reminder_system() -> None:
    """
    Test the medication reminder system with various scenarios.
    Verifies functionality and error handling.
    """
    print("=== Medication Reminder System Test ===\n")
    
    # Clear any existing reminders
    clear_all_reminders()
    print("Cleared existing reminders.\n")
    
    # Test 1: Add valid reminders
    print("Test 1: Adding valid reminders...")
    try:
        r1 = add_reminder("Aspirin", "08:30")
        print(f"  + Added: {r1['medicine_name']} at {r1['time']}")
        
        r2 = add_reminder("Vitamin D", "12:00")
        print(f"  + Added: {r2['medicine_name']} at {r2['time']}")
        
        r3 = add_reminder("Blood Pressure Medicine", "20:15")
        print(f"  + Added: {r3['medicine_name']} at {r3['time']}")
    except Exception as e:
        print(f"  ! Error: {str(e)}")
    print()
    
    # Test 2: Get all reminders
    print("Test 2: Retrieving all reminders...")
    try:
        all_reminders = get_all_reminders()
        print(f"  + Found {len(all_reminders)} reminders:")
        for reminder in all_reminders:
            print(f"    - ID:{reminder['id']} {reminder['medicine_name']} at {reminder['time']}")
    except Exception as e:
        print(f"  ! Error: {str(e)}")
    print()
    
    # Test 3: Delete a reminder
    print("Test 3: Deleting a reminder...")
    try:
        deleted = delete_reminder(2)
        if deleted:
            print("  + Reminder deleted successfully")
        else:
            print("  - Reminder not found")
        
        remaining = get_all_reminders()
        print(f"  + Remaining reminders: {len(remaining)}")
    except Exception as e:
        print(f"  ! Error: {str(e)}")
    print()
    
    # Test 4: Test error handling (empty input)
    print("Test 4: Testing error handling...")
    try:
        add_reminder("", "10:00")
        print("  ! Should have raised error for empty medicine name")
    except ValueError as e:
        print(f"  + Correctly caught error: {str(e)}")
    
    try:
        add_reminder("Aspirin", "25:99")
        print("  ! Should have raised error for invalid time")
    except ValueError as e:
        print(f"  + Correctly caught error: {str(e)}")
    print()
    
    print("=== Test Complete ===")

if __name__ == "__main__":
    test_reminder_system()
