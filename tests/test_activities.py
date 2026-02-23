"""
Tests for the activities endpoint (GET /activities).
"""

import pytest


class TestGetActivities:
    """Tests for retrieving the activities list."""

    def test_get_activities_returns_200(self, client):
        """Verify GET /activities returns a 200 status code."""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_all_activities(self, client):
        """Verify GET /activities returns all 9 activities."""
        response = client.get("/activities")
        data = response.json()
        assert len(data) == 9
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
        assert "Basketball Team" in data
        assert "Tennis Club" in data
        assert "Drama Club" in data
        assert "Art Studio" in data
        assert "Debate Team" in data
        assert "Science Club" in data

    def test_get_activities_has_required_keys(self, client):
        """Verify each activity has required keys."""
        response = client.get("/activities")
        data = response.json()
        
        required_keys = {"description", "schedule", "max_participants", "participants"}
        
        for activity_name, activity_details in data.items():
            assert set(activity_details.keys()) == required_keys, \
                f"Activity '{activity_name}' missing required keys"

    def test_get_activities_participants_is_list(self, client):
        """Verify participants field is always a list."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_details in data.items():
            assert isinstance(activity_details["participants"], list), \
                f"Activity '{activity_name}' participants should be a list"

    def test_get_activities_with_participants(self, client):
        """Verify activities with participants show correct data."""
        response = client.get("/activities")
        data = response.json()
        
        # Chess Club has 2 participants
        assert len(data["Chess Club"]["participants"]) == 2
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in data["Chess Club"]["participants"]

    def test_get_activities_with_no_participants(self, client):
        """Verify activities with no participants show empty list."""
        response = client.get("/activities")
        data = response.json()
        
        # Basketball Team has no participants
        assert len(data["Basketball Team"]["participants"]) == 0
        assert data["Basketball Team"]["participants"] == []

    def test_get_activities_max_participants_field(self, client):
        """Verify max_participants field is present and integer."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_details in data.items():
            assert isinstance(activity_details["max_participants"], int), \
                f"Activity '{activity_name}' max_participants should be an integer"
            assert activity_details["max_participants"] > 0, \
                f"Activity '{activity_name}' max_participants should be positive"

    def test_get_activities_schedule_field(self, client):
        """Verify schedule field is present and non-empty string."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_details in data.items():
            assert isinstance(activity_details["schedule"], str), \
                f"Activity '{activity_name}' schedule should be a string"
            assert len(activity_details["schedule"]) > 0, \
                f"Activity '{activity_name}' schedule should not be empty"

    def test_get_activities_description_field(self, client):
        """Verify description field is present and non-empty string."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_details in data.items():
            assert isinstance(activity_details["description"], str), \
                f"Activity '{activity_name}' description should be a string"
            assert len(activity_details["description"]) > 0, \
                f"Activity '{activity_name}' description should not be empty"

    def test_get_activities_returns_json(self, client):
        """Verify response is valid JSON."""
        response = client.get("/activities")
        assert response.headers["content-type"].startswith("application/json")
