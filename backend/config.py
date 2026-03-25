# -*- coding: utf-8 -*-
"""
Configuration settings for the Visual Wave Detection System
"""

import os

# Security settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-jwt-secret-change-in-production')

# Database settings
DATABASE_PATH = os.environ.get('DATABASE_PATH', 'wave_detection.db')

# Upload settings
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'mp4', 'avi', 'mov'}

# Wave detection settings
DEFAULT_SENSITIVITY = 0.5
MIN_WAVE_HEIGHT = 5  # pixels
MAX_WAVE_HEIGHT = 1000  # pixels
DETECTION_TIMEOUT = 30  # seconds

# AI Model settings
AI_MODEL_PATH = os.environ.get('AI_MODEL_PATH', 'models/wave_detection_model.pth')
