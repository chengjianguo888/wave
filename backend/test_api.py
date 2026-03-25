"""
API Testing Script
Quick script to test all API endpoints
"""

import requests
import json

BASE_URL = 'http://localhost:5000/api'


def test_health():
    """Test health endpoint"""
    response = requests.get(f'{BASE_URL}/health')
    print(f"Health Check: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200


def test_register():
    """Test user registration"""
    data = {
        'username': 'testuser',
        'password': 'testpass123',
        'email': 'test@example.com'
    }

    response = requests.post(f'{BASE_URL}/auth/register', json=data)
    print(f"\nRegister: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code in [201, 409]  # 409 if already exists


def test_login():
    """Test user login"""
    data = {
        'username': 'testuser',
        'password': 'testpass123'
    }

    response = requests.post(f'{BASE_URL}/auth/login', json=data)
    print(f"\nLogin: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(json.dumps(result, indent=2))
        return result.get('access_token')

    return None


def test_protected_endpoints(token):
    """Test protected endpoints with authentication"""
    headers = {'Authorization': f'Bearer {token}'}

    # Test profile
    response = requests.get(f'{BASE_URL}/user/profile', headers=headers)
    print(f"\nProfile: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))

    # Test algorithms list
    response = requests.get(f'{BASE_URL}/algorithms', headers=headers)
    print(f"\nAlgorithms: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))

    # Test stats
    response = requests.get(f'{BASE_URL}/stats/summary', headers=headers)
    print(f"\nStats: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))


if __name__ == '__main__':
    print("=" * 50)
    print("Visual Wave Detection System - API Test")
    print("=" * 50)

    # Test health
    if not test_health():
        print("\nError: Backend server is not running!")
        exit(1)

    # Test registration
    test_register()

    # Test login
    token = test_login()

    if token:
        # Test protected endpoints
        test_protected_endpoints(token)
        print("\n" + "=" * 50)
        print("All API tests completed successfully!")
        print("=" * 50)
    else:
        print("\nError: Login failed!")
