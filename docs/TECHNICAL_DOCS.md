# Visual Wave Detection System - Technical Documentation

## System Architecture

### Overview
The Visual Wave Detection System is a full-stack web application designed to detect and analyze wave patterns in images using computer vision techniques.

### Components

#### Backend (Flask)
- **app.py**: Main Flask application with REST API endpoints
- **database.py**: SQLite database abstraction layer
- **wave_detector.py**: Core wave detection engine with multiple algorithms
- **config.py**: Configuration management

#### Frontend (React)
- **Login.jsx**: Authentication interface
- **Dashboard.jsx**: Main application dashboard
- **WaveVisualizer.jsx**: Wave visualization and charting
- **DetectionHistory.jsx**: Historical data management

### Data Flow

```
User -> Frontend (React)
  |
  v
Authentication (JWT)
  |
  v
Backend API (Flask)
  |
  +-> Database (SQLite) <- User & Detection Data
  |
  +-> Wave Detector (OpenCV) <- Image Processing
  |
  v
Results -> Visualization -> User
```

## Wave Detection Algorithms

### 1. Edge Detection
**Algorithm**: Canny Edge Detector + Contour Analysis

**Steps**:
1. Convert image to grayscale
2. Apply Gaussian blur (5x5 kernel)
3. Canny edge detection with adaptive thresholds
4. Find contours using RETR_EXTERNAL mode
5. Filter contours by area (>100 pixels)
6. Calculate wave properties from bounding boxes

**Output Metrics**:
- Wave count: Number of detected contours
- Amplitude: Height of bounding box
- Wavelength: Width of bounding box
- Confidence: Heuristic based on wave count

**Complexity**: O(n*m) where n,m are image dimensions

### 2. Frequency Analysis
**Algorithm**: Fast Fourier Transform (FFT) + Peak Detection

**Steps**:
1. Convert to grayscale
2. Apply FFT to horizontal rows (sampled every 10th row)
3. Compute magnitude spectrum
4. Detect peaks in frequency domain
5. Extract dominant frequencies
6. Aggregate statistics across rows

**Output Metrics**:
- Wave count: Number of significant frequencies
- Frequency range: Min/max detected frequencies
- Amplitude: Peak magnitudes in frequency domain
- Confidence: Based on number of detected frequencies

**Complexity**: O(n*m*log(m)) for FFT operations

### 3. Optical Flow
**Algorithm**: Farneback Optical Flow + Connected Components

**Steps**:
1. Create synthetic frame pair (for static images)
2. Calculate dense optical flow field
3. Compute motion magnitude and angle
4. Threshold based on percentile
5. Find connected components in motion field
6. Extract wave regions

**Output Metrics**:
- Wave count: Number of motion regions
- Motion magnitude: Average flow strength
- Wave properties: Size and position of regions

**Complexity**: O(n*m) for optical flow computation

**Note**: Works better with actual video frames

### 4. AI Detection
**Algorithm**: Adaptive Thresholding + Morphological Analysis + Heuristic Scoring

**Steps**:
1. Resize to standard size (640x480)
2. Convert to grayscale
3. Adaptive thresholding (Gaussian method)
4. Morphological closing with elliptical kernel
5. Contour detection
6. Feature extraction (aspect ratio, circularity)
7. Confidence scoring based on wave-like properties

**Scoring Formula**:
```
confidence = 0.4 * aspect_ratio_score +
             0.3 * (1 - circularity) +
             0.3 * area_score
```

**Wave-like Properties**:
- Aspect ratio: 1.5 < ratio < 10 (elongated shapes)
- Low circularity (non-circular)
- Significant area

**Output Metrics**:
- Wave count: Number of wave-like contours
- Per-wave confidence scores
- Geometric properties

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Detections Table
```sql
CREATE TABLE detections (
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
```

## API Specifications

### Authentication Flow
1. User registers: POST /api/auth/register
2. Password hashed using Werkzeug (PBKDF2)
3. User logs in: POST /api/auth/login
4. JWT token generated with 24h expiry
5. Token included in Authorization header for protected endpoints

### Detection Flow
1. User uploads image: POST /api/detect/upload
2. File saved with user_id prefix
3. Detection algorithm executed
4. Results saved to database
5. Response includes detection_id and results
6. Results available in history

### Error Handling
All endpoints return consistent error format:
```json
{
  "error": "Error message description"
}
```

HTTP Status Codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 409: Conflict
- 500: Internal Server Error

## Security Considerations

### Authentication
- Passwords hashed with PBKDF2-SHA256
- JWT tokens with expiration
- Token-based API protection

### Input Validation
- File type validation
- File size limits (50MB)
- Filename sanitization
- SQL parameterized queries

### Best Practices
- Never commit .env files
- Rotate JWT secrets regularly
- Use HTTPS in production
- Rate limit API endpoints
- Sanitize file uploads

## Performance Optimization

### Backend
- Image processing optimized with OpenCV
- Database indexes on user_id and created_at
- Pagination for large datasets
- File upload size limits

### Frontend
- Lazy loading components
- Image preview optimization
- Debounced API calls
- Efficient re-rendering

## Deployment

### Docker Deployment
Recommended for production:
```bash
docker-compose up -d
```

Benefits:
- Isolated environment
- Easy scaling
- Consistent deployment
- Simple updates

### Manual Deployment
For development or custom setups:

1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run build
   npm run preview
   ```

### Production Considerations
- Use production WSGI server (Gunicorn)
- Configure nginx as reverse proxy
- Enable HTTPS with SSL certificates
- Set up database backups
- Configure logging and monitoring

## Testing Strategy

### Unit Tests
- Database operations (test_database.py)
- Wave detection algorithms (test_wave_detector.py)
- Run with: `pytest tests/`

### Integration Tests
- API endpoints (test_api.py)
- Authentication flow
- Detection workflow

### Manual Testing
1. Generate sample images: `python generate_samples.py`
2. Test API: `python test_api.py`
3. Test frontend manually through browser

## Extensibility

### Adding New Algorithms
1. Implement detection method in WaveDetector class
2. Register in algorithms dictionary
3. Add API documentation
4. Update frontend algorithm selector

### Adding New Features
- User management: Extend database.py
- New visualizations: Add to WaveVisualizer.jsx
- Export formats: Extend export methods
- Batch processing: Add new API endpoints

## Monitoring and Maintenance

### Logs
- Backend: Flask application logs
- Frontend: Browser console
- Database: SQLite logs

### Database Maintenance
- Regular backups recommended
- Periodic cleanup of old detections
- Index optimization for large datasets

### Updates
- Backend: Update requirements.txt versions
- Frontend: Update package.json versions
- Test thoroughly after updates
