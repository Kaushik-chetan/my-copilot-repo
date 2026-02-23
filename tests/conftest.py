"""
Pytest configuration and shared fixtures for the test suite.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient instance for making requests to the app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Reset activities to initial state before each test.
    This fixture runs automatically for all tests to ensure test isolation.
    """
    # Save initial state
    initial_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for interscholastic play",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": []
        },
        "Tennis Club": {
            "description": "Learn tennis skills and participate in matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 10,
            "participants": []
        },
        "Drama Club": {
            "description": "Act in school plays and develop theatrical skills",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": []
        },
        "Art Studio": {
            "description": "Painting, drawing, and sculpture techniques",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": []
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Mondays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": []
        },
        "Science Club": {
            "description": "Explore scientific research and conduct experiments",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": []
        }
    }
    
    # Clear current activities
    activities.clear()
    
    # Restore initial state
    activities.update(initial_activities)
    
    yield  # Tests run here
    
    # Cleanup after test (optional, but good practice)
    activities.clear()
    activities.update(initial_activities)
