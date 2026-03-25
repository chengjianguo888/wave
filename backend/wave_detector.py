# -*- coding: utf-8 -*-
"""
Wave Detection Engine
Implements multiple algorithms for visual wave detection
"""

import cv2
import numpy as np
import base64
from typing import Dict, List, Tuple
from scipy import signal
from scipy.fft import fft, fftfreq
import json


class WaveDetector:
    """Main wave detection engine with multiple algorithm support"""

    def __init__(self):
        self.algorithms = {
            'edge_detection': self._edge_detection,
            'frequency_analysis': self._frequency_analysis,
            'optical_flow': self._optical_flow,
            'ai_detection': self._ai_detection
        }

    def detect(self, filepath: str, algorithm: str = 'edge_detection', **kwargs) -> Dict:
        """
        Detect waves in an image or video file

        Args:
            filepath: Path to the image or video file
            algorithm: Detection algorithm to use
            **kwargs: Additional parameters for the algorithm

        Returns:
            Dictionary containing detection results
        """
        # Read image
        image = cv2.imread(filepath)
        if image is None:
            raise ValueError('Failed to read image file')

        # Select and run algorithm
        if algorithm not in self.algorithms:
            raise ValueError(f'Unknown algorithm: {algorithm}')

        detection_func = self.algorithms[algorithm]
        result = detection_func(image, **kwargs)

        # Add metadata
        result['image_shape'] = image.shape
        result['algorithm'] = algorithm
        result['filepath'] = filepath

        return result

    def detect_from_base64(self, image_data: str, algorithm: str = 'edge_detection', **kwargs) -> Dict:
        """
        Detect waves from base64 encoded image data

        Args:
            image_data: Base64 encoded image
            algorithm: Detection algorithm to use
            **kwargs: Additional parameters for the algorithm

        Returns:
            Dictionary containing detection results
        """
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError('Failed to decode image data')

        # Select and run algorithm
        if algorithm not in self.algorithms:
            raise ValueError(f'Unknown algorithm: {algorithm}')

        detection_func = self.algorithms[algorithm]
        result = detection_func(image, **kwargs)

        # Add metadata
        result['image_shape'] = image.shape
        result['algorithm'] = algorithm

        return result

    def _edge_detection(self, image: np.ndarray, sensitivity: float = 0.5, **kwargs) -> Dict:
        """
        Edge detection based wave detection using Canny algorithm
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Canny edge detection
        threshold1 = int(50 * sensitivity)
        threshold2 = int(150 * sensitivity)
        edges = cv2.Canny(blurred, threshold1, threshold2)

        # Find contours (wave boundaries)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Analyze wave patterns
        waves = []
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # Filter small noise
                x, y, w, h = cv2.boundingRect(contour)
                amplitude = h
                wavelength = w

                waves.append({
                    'position': {'x': int(x), 'y': int(y)},
                    'amplitude': float(amplitude),
                    'wavelength': float(wavelength),
                    'area': float(cv2.contourArea(contour))
                })

        # Calculate statistics
        wave_count = len(waves)
        avg_amplitude = np.mean([w['amplitude'] for w in waves]) if waves else 0.0
        avg_wavelength = np.mean([w['wavelength'] for w in waves]) if waves else 0.0
        confidence_score = min(1.0, wave_count * 0.05)  # Heuristic confidence

        return {
            'wave_count': wave_count,
            'avg_amplitude': float(avg_amplitude),
            'avg_frequency': float(1.0 / avg_wavelength if avg_wavelength > 0 else 0),
            'confidence_score': float(confidence_score),
            'waves': waves[:50],  # Limit to first 50 waves for response size
            'detection_method': 'edge_detection'
        }

    def _frequency_analysis(self, image: np.ndarray, sensitivity: float = 0.5, **kwargs) -> Dict:
        """
        Frequency domain analysis for wave detection using FFT
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply FFT to each row to find horizontal wave patterns
        height, width = gray.shape
        frequencies = []
        amplitudes = []

        # Sample rows for analysis (every 10th row to reduce computation)
        for i in range(0, height, 10):
            row = gray[i, :]

            # Perform FFT
            fft_vals = fft(row)
            fft_freq = fftfreq(len(row))

            # Get magnitude spectrum
            magnitude = np.abs(fft_vals)

            # Find peaks in frequency domain
            peaks, properties = signal.find_peaks(magnitude[1:len(magnitude)//2],
                                                   height=np.max(magnitude) * sensitivity * 0.1)

            if len(peaks) > 0:
                dominant_freq_idx = peaks[np.argmax(properties['peak_heights'])]
                frequencies.append(abs(fft_freq[dominant_freq_idx + 1]))
                amplitudes.append(properties['peak_heights'][np.argmax(properties['peak_heights'])])

        # Calculate statistics
        wave_count = len(frequencies)
        avg_frequency = np.mean(frequencies) if frequencies else 0.0
        avg_amplitude = np.mean(amplitudes) if amplitudes else 0.0
        confidence_score = min(1.0, wave_count * 0.03)

        return {
            'wave_count': wave_count,
            'avg_amplitude': float(avg_amplitude),
            'avg_frequency': float(avg_frequency),
            'confidence_score': float(confidence_score),
            'frequency_range': {
                'min': float(min(frequencies)) if frequencies else 0.0,
                'max': float(max(frequencies)) if frequencies else 0.0
            },
            'detection_method': 'frequency_analysis'
        }

    def _optical_flow(self, image: np.ndarray, sensitivity: float = 0.5, **kwargs) -> Dict:
        """
        Optical flow based wave motion detection
        Note: This is simplified for static images; works better with video frames
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Create a synthetic previous frame by shifting the image
        # In real implementation, this would use actual video frames
        height, width = gray.shape
        shift = int(width * 0.02)  # 2% shift
        prev_gray = np.roll(gray, shift, axis=1)

        # Calculate optical flow
        flow = cv2.calcOpticalFlowFarneback(
            prev_gray, gray, None,
            pyr_scale=0.5, levels=3, winsize=15,
            iterations=3, poly_n=5, poly_sigma=1.2, flags=0
        )

        # Analyze flow patterns
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])

        # Detect wave-like motion patterns
        threshold = np.percentile(magnitude, 90 * (1 - sensitivity))
        wave_regions = magnitude > threshold

        # Find connected components (wave regions)
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
            wave_regions.astype(np.uint8), connectivity=8
        )

        waves = []
        for i in range(1, num_labels):  # Skip background
            area = stats[i, cv2.CC_STAT_AREA]
            if area > 50:  # Filter small regions
                x = stats[i, cv2.CC_STAT_LEFT]
                y = stats[i, cv2.CC_STAT_TOP]
                w = stats[i, cv2.CC_STAT_WIDTH]
                h = stats[i, cv2.CC_STAT_HEIGHT]

                waves.append({
                    'position': {'x': int(x), 'y': int(y)},
                    'amplitude': float(h),
                    'wavelength': float(w),
                    'area': float(area),
                    'motion_magnitude': float(np.mean(magnitude[labels == i]))
                })

        wave_count = len(waves)
        avg_amplitude = np.mean([w['amplitude'] for w in waves]) if waves else 0.0
        avg_wavelength = np.mean([w['wavelength'] for w in waves]) if waves else 0.0
        confidence_score = min(1.0, wave_count * 0.04)

        return {
            'wave_count': wave_count,
            'avg_amplitude': float(avg_amplitude),
            'avg_frequency': float(1.0 / avg_wavelength if avg_wavelength > 0 else 0),
            'confidence_score': float(confidence_score),
            'waves': waves[:50],
            'detection_method': 'optical_flow'
        }

    def _ai_detection(self, image: np.ndarray, sensitivity: float = 0.5, **kwargs) -> Dict:
        """
        AI-based wave detection using deep learning
        Note: This is a simulated implementation. In production, would use a trained model.
        """
        # Preprocess image
        resized = cv2.resize(image, (640, 480))
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

        # Simulate AI detection with advanced image processing
        # In production, this would use a trained CNN/YOLO model

        # Use adaptive thresholding for wave-like patterns
        adaptive_thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 11, 2
        )

        # Apply morphological operations to identify wave structures
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        morph = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)

        # Find contours
        contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Classify and score wave patterns
        waves = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 200:  # Filter noise
                x, y, w, h = cv2.boundingRect(contour)

                # Calculate wave characteristics
                aspect_ratio = w / h if h > 0 else 0
                perimeter = cv2.arcLength(contour, True)
                circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0

                # Heuristic confidence based on wave-like properties
                wave_confidence = (
                    0.4 * (1.0 if 1.5 < aspect_ratio < 10 else 0.5) +  # Waves are typically elongated
                    0.3 * (1.0 - circularity) +  # Waves are not circular
                    0.3 * min(1.0, area / 10000)  # Larger waves are more confident
                )

                waves.append({
                    'position': {'x': int(x), 'y': int(y)},
                    'amplitude': float(h),
                    'wavelength': float(w),
                    'area': float(area),
                    'confidence': float(wave_confidence),
                    'properties': {
                        'aspect_ratio': float(aspect_ratio),
                        'circularity': float(circularity)
                    }
                })

        # Sort by confidence
        waves.sort(key=lambda w: w['confidence'], reverse=True)

        wave_count = len(waves)
        avg_amplitude = np.mean([w['amplitude'] for w in waves]) if waves else 0.0
        avg_wavelength = np.mean([w['wavelength'] for w in waves]) if waves else 0.0
        avg_confidence = np.mean([w['confidence'] for w in waves]) if waves else 0.0

        return {
            'wave_count': wave_count,
            'avg_amplitude': float(avg_amplitude),
            'avg_frequency': float(1.0 / avg_wavelength if avg_wavelength > 0 else 0),
            'confidence_score': float(avg_confidence),
            'waves': waves[:50],
            'detection_method': 'ai_detection'
        }

    def export_to_csv(self, detection: Dict) -> str:
        """Export detection result to CSV format"""
        csv_lines = ['Wave ID,Position X,Position Y,Amplitude,Wavelength,Area,Confidence']

        result_data = json.loads(detection.get('result_json', '{}'))
        waves = result_data.get('waves', [])

        for idx, wave in enumerate(waves):
            pos = wave.get('position', {})
            csv_lines.append(
                f"{idx},{pos.get('x', 0)},{pos.get('y', 0)},"
                f"{wave.get('amplitude', 0)},{wave.get('wavelength', 0)},"
                f"{wave.get('area', 0)},{wave.get('confidence', 0)}"
            )

        return '\n'.join(csv_lines)
