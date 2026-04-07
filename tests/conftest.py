import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Provide a TestClient for making requests to the app."""
    return TestClient(app)


@pytest.fixture
def test_activities():
    """Provide clean test data for each test."""
    return {
        "Math Club": {
            "description": "Explore advanced mathematics",
            "schedule": "Mondays, 3:30 PM - 4:30 PM",
            "max_participants": 15,
            "participants": ["alice@test.edu", "bob@test.edu"]
        },
        "Art Class": {
            "description": "Create beautiful artwork",
            "schedule": "Wednesdays, 4:00 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["charlie@test.edu"]
        },
        "Chess Club": {
            "description": "Play strategic chess games",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 2,
            "participants": ["david@test.edu", "eve@test.edu"]
        }
    }


@pytest.fixture
def app_with_test_data(test_activities, monkeypatch):
    """Monkeypatch the app's activities with test data for isolation."""
    monkeypatch.setattr("src.app.activities", test_activities)
    return TestClient(app)
