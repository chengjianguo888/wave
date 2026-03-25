"""
Tests for the wave detection system
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wave_detector import WaveDetector
import numpy as np
import cv2


@pytest.fixture
def wave_detector():
    return WaveDetector()


@pytest.fixture
def sample_image():
    """Create a synthetic wave image for testing"""
    # Create a simple sinusoidal wave pattern
    width, height = 640, 480
    image = np.zeros((height, width, 3), dtype=np.uint8)

    # Generate wave pattern
    for x in range(width):
        y = int(height / 2 + 50 * np.sin(2 * np.pi * x / 100))
        if 0 <= y < height:
            cv2.circle(image, (x, y), 2, (255, 255, 255), -1)

    return image


def test_edge_detection(wave_detector, sample_image):
    """Test edge detection algorithm"""
    # Save temporary image
    temp_path = '/tmp/test_wave.png'
    cv2.imwrite(temp_path, sample_image)

    result = wave_detector.detect(temp_path, algorithm='edge_detection', sensitivity=0.5)

    assert 'wave_count' in result
    assert 'avg_amplitude' in result
    assert 'avg_frequency' in result
    assert 'confidence_score' in result
    assert result['algorithm'] == 'edge_detection'
    assert isinstance(result['wave_count'], int)

    # Clean up
    os.remove(temp_path)


def test_frequency_analysis(wave_detector, sample_image):
    """Test frequency analysis algorithm"""
    temp_path = '/tmp/test_wave.png'
    cv2.imwrite(temp_path, sample_image)

    result = wave_detector.detect(temp_path, algorithm='frequency_analysis', sensitivity=0.5)

    assert 'wave_count' in result
    assert result['algorithm'] == 'frequency_analysis'
    assert 'frequency_range' in result

    os.remove(temp_path)


def test_optical_flow(wave_detector, sample_image):
    """Test optical flow algorithm"""
    temp_path = '/tmp/test_wave.png'
    cv2.imwrite(temp_path, sample_image)

    result = wave_detector.detect(temp_path, algorithm='optical_flow', sensitivity=0.5)

    assert 'wave_count' in result
    assert result['algorithm'] == 'optical_flow'

    os.remove(temp_path)


def test_ai_detection(wave_detector, sample_image):
    """Test AI detection algorithm"""
    temp_path = '/tmp/test_wave.png'
    cv2.imwrite(temp_path, sample_image)

    result = wave_detector.detect(temp_path, algorithm='ai_detection', sensitivity=0.5)

    assert 'wave_count' in result
    assert result['algorithm'] == 'ai_detection'

    os.remove(temp_path)


def test_invalid_algorithm(wave_detector):
    """Test that invalid algorithm raises error"""
    with pytest.raises(ValueError, match='Unknown algorithm'):
        wave_detector.detect('/tmp/test.png', algorithm='invalid_algorithm')


def test_csv_export(wave_detector):
    """Test CSV export functionality"""
    detection = {
        'result_json': '{"waves": [{"position": {"x": 10, "y": 20}, "amplitude": 30, "wavelength": 40, "area": 500, "confidence": 0.9}]}'
    }

    csv_result = wave_detector.export_to_csv(detection)

    assert 'Wave ID' in csv_result
    assert 'Position X' in csv_result
    assert '10,20,30,40,500' in csv_result
