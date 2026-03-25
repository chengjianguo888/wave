"""
Visual Wave Detection System - Backend API
Main Flask application with authentication and wave detection endpoints
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import timedelta
from database import Database
from wave_detector import WaveDetector
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

CORS(app)
jwt = JWTManager(app)

db = Database()
wave_detector = WaveDetector()

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'version': '1.0.0'}), 200


@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password or not email:
            return jsonify({'error': 'Missing required fields'}), 400

        # Check if user already exists
        existing_user = db.get_user_by_username(username)
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 409

        # Hash password and create user
        password_hash = generate_password_hash(password)
        user_id = db.create_user(username, password_hash, email)

        if user_id:
            return jsonify({
                'message': 'User registered successfully',
                'user_id': user_id
            }), 201
        else:
            return jsonify({'error': 'Failed to create user'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Missing credentials'}), 400

        # Verify user credentials
        user = db.get_user_by_username(username)
        if not user or not check_password_hash(user['password_hash'], password):
            return jsonify({'error': 'Invalid credentials'}), 401

        # Create access token
        access_token = create_access_token(identity=user['id'])

        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        user_id = get_jwt_identity()
        user = db.get_user_by_id(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'created_at': user['created_at']
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/detect/upload', methods=['POST'])
@jwt_required()
def upload_and_detect():
    """Upload image/video and perform wave detection"""
    try:
        user_id = get_jwt_identity()

        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400

        # Get detection parameters
        algorithm = request.form.get('algorithm', 'edge_detection')
        sensitivity = float(request.form.get('sensitivity', 0.5))

        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{user_id}_{filename}")
        file.save(filepath)

        # Perform wave detection
        result = wave_detector.detect(filepath, algorithm=algorithm, sensitivity=sensitivity)

        # Save detection result to database
        detection_id = db.save_detection(
            user_id=user_id,
            filename=filename,
            algorithm=algorithm,
            result_data=result
        )

        return jsonify({
            'detection_id': detection_id,
            'result': result
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/detect/realtime', methods=['POST'])
@jwt_required()
def realtime_detect():
    """Real-time wave detection from base64 image data"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        image_data = data.get('image_data')
        algorithm = data.get('algorithm', 'edge_detection')
        sensitivity = data.get('sensitivity', 0.5)

        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400

        # Perform detection on base64 data
        result = wave_detector.detect_from_base64(
            image_data,
            algorithm=algorithm,
            sensitivity=sensitivity
        )

        return jsonify({'result': result}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/detections/history', methods=['GET'])
@jwt_required()
def get_detection_history():
    """Get user's detection history"""
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        detections = db.get_user_detections(user_id, page=page, per_page=per_page)
        total = db.get_user_detections_count(user_id)

        return jsonify({
            'detections': detections,
            'total': total,
            'page': page,
            'per_page': per_page
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/detections/<int:detection_id>', methods=['GET'])
@jwt_required()
def get_detection_detail(detection_id):
    """Get detailed detection result"""
    try:
        user_id = get_jwt_identity()
        detection = db.get_detection(detection_id)

        if not detection:
            return jsonify({'error': 'Detection not found'}), 404

        if detection['user_id'] != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        return jsonify(detection), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/detections/<int:detection_id>/export', methods=['GET'])
@jwt_required()
def export_detection(detection_id):
    """Export detection result as JSON or CSV"""
    try:
        user_id = get_jwt_identity()
        export_format = request.args.get('format', 'json')

        detection = db.get_detection(detection_id)

        if not detection:
            return jsonify({'error': 'Detection not found'}), 404

        if detection['user_id'] != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        if export_format == 'json':
            return jsonify(detection), 200
        elif export_format == 'csv':
            # Export as CSV
            csv_data = wave_detector.export_to_csv(detection)
            return csv_data, 200, {
                'Content-Type': 'text/csv',
                'Content-Disposition': f'attachment; filename=detection_{detection_id}.csv'
            }
        else:
            return jsonify({'error': 'Invalid export format'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/algorithms', methods=['GET'])
@jwt_required()
def get_algorithms():
    """Get list of available detection algorithms"""
    algorithms = [
        {
            'id': 'edge_detection',
            'name': 'Edge Detection',
            'description': 'Classical edge detection using Canny algorithm for wave boundary identification',
            'parameters': ['sensitivity']
        },
        {
            'id': 'frequency_analysis',
            'name': 'Frequency Analysis',
            'description': 'FFT-based frequency domain analysis for wave pattern detection',
            'parameters': ['sensitivity', 'frequency_range']
        },
        {
            'id': 'optical_flow',
            'name': 'Optical Flow',
            'description': 'Motion-based wave detection using optical flow algorithms',
            'parameters': ['sensitivity', 'flow_threshold']
        },
        {
            'id': 'ai_detection',
            'name': 'AI-Based Detection',
            'description': 'Deep learning model for intelligent wave pattern recognition',
            'parameters': ['sensitivity', 'confidence_threshold']
        }
    ]
    return jsonify({'algorithms': algorithms}), 200


@app.route('/api/stats/summary', methods=['GET'])
@jwt_required()
def get_stats_summary():
    """Get user statistics summary"""
    try:
        user_id = get_jwt_identity()
        stats = db.get_user_stats(user_id)

        return jsonify(stats), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    db.initialize()
    app.run(host='0.0.0.0', port=5000, debug=True)
