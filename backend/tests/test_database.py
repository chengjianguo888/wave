"""
Tests for database operations
"""

import pytest
import sys
import os
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import Database


@pytest.fixture
def db():
    """Create a temporary database for testing"""
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_db.close()

    database = Database(temp_db.name)
    database.initialize()

    yield database

    # Clean up
    os.unlink(temp_db.name)


def test_create_user(db):
    """Test user creation"""
    user_id = db.create_user('testuser', 'hashed_password', 'test@example.com')

    assert user_id is not None
    assert user_id > 0


def test_get_user_by_username(db):
    """Test retrieving user by username"""
    db.create_user('testuser', 'hashed_password', 'test@example.com')

    user = db.get_user_by_username('testuser')

    assert user is not None
    assert user['username'] == 'testuser'
    assert user['email'] == 'test@example.com'


def test_get_user_by_id(db):
    """Test retrieving user by ID"""
    user_id = db.create_user('testuser', 'hashed_password', 'test@example.com')

    user = db.get_user_by_id(user_id)

    assert user is not None
    assert user['id'] == user_id


def test_duplicate_username(db):
    """Test that duplicate usernames are prevented"""
    db.create_user('testuser', 'hashed_password', 'test@example.com')
    result = db.create_user('testuser', 'different_hash', 'other@example.com')

    assert result is None


def test_save_detection(db):
    """Test saving detection results"""
    user_id = db.create_user('testuser', 'hashed_password', 'test@example.com')

    result_data = {
        'wave_count': 10,
        'avg_amplitude': 25.5,
        'avg_frequency': 0.05,
        'confidence_score': 0.85
    }

    detection_id = db.save_detection(user_id, 'test.jpg', 'edge_detection', result_data)

    assert detection_id is not None
    assert detection_id > 0


def test_get_detection(db):
    """Test retrieving detection by ID"""
    user_id = db.create_user('testuser', 'hashed_password', 'test@example.com')

    result_data = {
        'wave_count': 10,
        'avg_amplitude': 25.5
    }

    detection_id = db.save_detection(user_id, 'test.jpg', 'edge_detection', result_data)
    detection = db.get_detection(detection_id)

    assert detection is not None
    assert detection['user_id'] == user_id
    assert detection['wave_count'] == 10


def test_get_user_detections(db):
    """Test getting user's detection history"""
    user_id = db.create_user('testuser', 'hashed_password', 'test@example.com')

    # Create multiple detections
    for i in range(5):
        db.save_detection(user_id, f'test{i}.jpg', 'edge_detection', {'wave_count': i})

    detections = db.get_user_detections(user_id, page=1, per_page=10)

    assert len(detections) == 5


def test_get_user_stats(db):
    """Test getting user statistics"""
    user_id = db.create_user('testuser', 'hashed_password', 'test@example.com')

    # Create detections
    db.save_detection(user_id, 'test1.jpg', 'edge_detection', {
        'wave_count': 10,
        'confidence_score': 0.8
    })
    db.save_detection(user_id, 'test2.jpg', 'ai_detection', {
        'wave_count': 5,
        'confidence_score': 0.9
    })

    stats = db.get_user_stats(user_id)

    assert stats['total_detections'] == 2
    assert stats['total_waves'] == 15
    assert stats['avg_confidence'] > 0
