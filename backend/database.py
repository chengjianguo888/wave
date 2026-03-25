"""
Database layer for Visual Wave Detection System
Handles user management and detection history
"""

import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict


class Database:
    def __init__(self, db_path='wave_detection.db'):
        self.db_path = db_path

    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Detections table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                algorithm TEXT NOT NULL,
                wave_count INTEGER,
                avg_amplitude REAL,
                avg_frequency REAL,
                confidence_score REAL,
                result_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        conn.commit()
        conn.close()

    def create_user(self, username: str, password_hash: str, email: str) -> Optional[int]:
        """Create a new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)',
                (username, password_hash, email)
            )
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            return None

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def save_detection(self, user_id: int, filename: str, algorithm: str, result_data: Dict) -> int:
        """Save detection result"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO detections
            (user_id, filename, algorithm, wave_count, avg_amplitude, avg_frequency, confidence_score, result_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            filename,
            algorithm,
            result_data.get('wave_count', 0),
            result_data.get('avg_amplitude', 0.0),
            result_data.get('avg_frequency', 0.0),
            result_data.get('confidence_score', 0.0),
            json.dumps(result_data)
        ))

        detection_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return detection_id

    def get_detection(self, detection_id: int) -> Optional[Dict]:
        """Get detection by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM detections WHERE id = ?', (detection_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            result = dict(row)
            if result['result_json']:
                result['result_data'] = json.loads(result['result_json'])
            return result
        return None

    def get_user_detections(self, user_id: int, page: int = 1, per_page: int = 10) -> List[Dict]:
        """Get user's detection history with pagination"""
        conn = self.get_connection()
        cursor = conn.cursor()

        offset = (page - 1) * per_page
        cursor.execute('''
            SELECT id, filename, algorithm, wave_count, avg_amplitude,
                   avg_frequency, confidence_score, created_at
            FROM detections
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        ''', (user_id, per_page, offset))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_user_detections_count(self, user_id: int) -> int:
        """Get total count of user's detections"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM detections WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result['count'] if result else 0

    def get_user_stats(self, user_id: int) -> Dict:
        """Get user statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                COUNT(*) as total_detections,
                SUM(wave_count) as total_waves,
                AVG(confidence_score) as avg_confidence,
                MAX(created_at) as last_detection
            FROM detections
            WHERE user_id = ?
        ''', (user_id,))

        result = cursor.fetchone()
        conn.close()

        if result:
            return dict(result)
        return {
            'total_detections': 0,
            'total_waves': 0,
            'avg_confidence': 0.0,
            'last_detection': None
        }
