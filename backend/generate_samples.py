# -*- coding: utf-8 -*-
"""
Utility script to generate sample wave images for testing
"""

import cv2
import numpy as np
import os


def generate_sine_wave_image(width=800, height=600, num_waves=3, output_path='sample_wave.png'):
    """Generate an image with sinusoidal wave patterns"""
    image = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background

    colors = [
        (255, 0, 0),    # Blue
        (0, 255, 0),    # Green
        (0, 0, 255),    # Red
    ]

    for i in range(num_waves):
        amplitude = 40 + i * 20
        frequency = 0.01 + i * 0.005
        phase = i * np.pi / 3
        color = colors[i % len(colors)]

        for x in range(width):
            y = int(height / 2 + amplitude * np.sin(2 * np.pi * frequency * x + phase))
            if 0 <= y < height:
                cv2.circle(image, (x, y), 3, color, -1)

    cv2.imwrite(output_path, image)
    print(f"Generated sample wave image: {output_path}")
    return output_path


def generate_ocean_wave_image(width=800, height=600, output_path='ocean_wave.png'):
    """Generate a more realistic ocean wave pattern"""
    image = np.zeros((height, width, 3), dtype=np.uint8)

    # Create gradient background (sky to water)
    for y in range(height):
        ratio = y / height
        if ratio < 0.3:  # Sky
            color = (200, 150, 100)  # Light blue
        else:  # Water
            color = (150, 100, 50)  # Blue
        image[y, :] = color

    # Add wave patterns
    for wave_idx in range(5):
        base_y = int(height * (0.4 + wave_idx * 0.12))
        amplitude = 15 + wave_idx * 5
        frequency = 0.015

        points = []
        for x in range(width):
            y = int(base_y + amplitude * np.sin(2 * np.pi * frequency * x + wave_idx))
            if 0 <= y < height:
                points.append([x, y])

        if points:
            points = np.array(points, dtype=np.int32)
            cv2.polylines(image, [points], False, (255, 255, 255), 2)

    cv2.imwrite(output_path, image)
    print(f"Generated ocean wave image: {output_path}")
    return output_path


def generate_ripple_pattern(width=800, height=600, output_path='ripple_wave.png'):
    """Generate circular ripple wave patterns"""
    image = np.ones((height, width, 3), dtype=np.uint8) * 200  # Light gray background

    # Generate concentric circles (ripples)
    center_x, center_y = width // 2, height // 2

    for radius in range(20, min(width, height) // 2, 30):
        cv2.circle(image, (center_x, center_y), radius, (100, 100, 100), 2)

    cv2.imwrite(output_path, image)
    print(f"Generated ripple pattern: {output_path}")
    return output_path


if __name__ == '__main__':
    # Create samples directory
    samples_dir = 'samples'
    os.makedirs(samples_dir, exist_ok=True)

    # Generate different types of wave images
    generate_sine_wave_image(output_path=os.path.join(samples_dir, 'sine_wave.png'))
    generate_ocean_wave_image(output_path=os.path.join(samples_dir, 'ocean_wave.png'))
    generate_ripple_pattern(output_path=os.path.join(samples_dir, 'ripple_wave.png'))

    print("\nSample images generated successfully!")
    print(f"Location: {os.path.abspath(samples_dir)}")
