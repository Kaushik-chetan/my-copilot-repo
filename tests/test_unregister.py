"""
Tests for the activity unregister endpoint (POST /activities/{activity_name}/unregister).
"""

import pytest


class TestUnregister:
    """Tests for unregistering students from activities."""

    def test_unregister_success(self, client):
        """Verify a student can successfully unregister from an activity."""
        # Michael is already in Chess Club
        response = client.post(
            "/activities/Chess%20Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "michael@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]

    def test_unregister_removes_from_participants_list(self, client):
        """Verify unregister actually removes student from participants list."""
        # Michael is in Chess Club
        response_before = client.get("/activities")
        data_before = response_before.json()
        assert "michael@mergington.edu" in data_before["Chess Club"]["participants"]
        assert len(data_before["Chess Club"]["participants"]) == 2
        
        # Unregister Michael
        client.post(
            "/activities/Chess%20Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        
        # Verify removed
        response_after = client.get("/activities")
        data_after = response_after.json()
        assert "michael@mergington.edu" not in data_after["Chess Club"]["participants"]
        assert len(data_after["Chess Club"]["participants"]) == 1

    def test_unregister_all_participants(self, client):
        """Verify activity can have all participants unregistered."""
        # Chess Club has 2 participants
        response = client.get("/activities")
        data = response.json()
        initial_participants = data["Chess Club"]["participants"].copy()
        assert len(initial_participants) == 2
        
        # Unregister each participant
        for email in initial_participants:
            response = client.post(
                "/activities/Chess%20Club/unregister",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify all removed
        response_after = client.get("/activities")
        data_after = response_after.json()
        assert len(data_after["Chess Club"]["participants"]) == 0

    def test_unregister_activity_not_found(self, client):
        """Verify unregister returns 404 for non-existent activity."""
        response = client.post(
            "/activities/Nonexistent%20Activity/unregister",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_not_registered(self, client):
        """Verify student cannot unregister from activity they're not in."""
        response = client.post(
            "/activities/Chess%20Club/unregister",
            params={"email": "notregistered@mergington.edu"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"]

    def test_unregister_from_empty_activity(self, client):
        """Verify unregister from activity with no participants fails."""
        # Basketball Team has no participants
        response = client.post(
            "/activities/Basketball%20Team/unregister",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"]

    def test_unregister_response_format(self, client):
        """Verify unregister response has correct format."""
        response = client.post(
            "/activities/Chess%20Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        data = response.json()
        assert "message" in data
        assert isinstance(data["message"], str)
        assert len(data["message"]) > 0

    def test_unregister_twice(self, client):
        """Verify student cannot unregister twice from same activity."""
        email = "michael@mergington.edu"
        
        # First unregister should succeed
        response1 = client.post(
            "/activities/Chess%20Club/unregister",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Second unregister should fail
        response2 = client.post(
            "/activities/Chess%20Club/unregister",
            params={"email": email}
        )
        assert response2.status_code == 400
        data = response2.json()
        assert "not signed up" in data["detail"]

    def test_unregister_then_signup_again(self, client):
        """Verify student can sign up again after unregistering."""
        email = "michael@mergington.edu"
        
        # Unregister (Michael is initially in Chess Club)
        response1 = client.post(
            "/activities/Chess%20Club/unregister",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Verify removed
        response_check = client.get("/activities")
        data_check = response_check.json()
        assert email not in data_check["Chess Club"]["participants"]
        
        # Sign up again
        response2 = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": email}
        )
        assert response2.status_code == 200
        
        # Verify back in list
        response_verify = client.get("/activities")
        data_verify = response_verify.json()
        assert email in data_verify["Chess Club"]["participants"]

    def test_unregister_case_sensitivity_email(self, client):
        """Verify email matching is case-sensitive in unregister."""
        # Try to unregister with different case than stored
        response = client.post(
            "/activities/Chess%20Club/unregister",
            params={"email": "MICHAEL@MERGINGTON.EDU"}  # uppercase
        )
        # Should fail because email is case-sensitive
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"]

    def test_unregister_activity_name_case_sensitivity(self, client):
        """Verify activity name lookup is case-sensitive."""
        # Wrong case should not find activity
        response = client.post(
            "/activities/chess%20club/unregister",  # lowercase 'c'
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 404

    def test_unregister_signup_workflow(self, client):
        """Verify complete signup/unregister workflow."""
        email = "workflow@mergington.edu"
        activity = "Tennis%20Club"
        
        # Verify not signed up initially
        response = client.get("/activities")
        data = response.json()
        assert email not in data["Tennis Club"]["participants"]
        
        # Sign up
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200
        
        # Verify signed up
        response = client.get("/activities")
        data = response.json()
        assert email in data["Tennis Club"]["participants"]
        
        # Unregister
        unregister_response = client.post(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        assert unregister_response.status_code == 200
        
        # Verify unregistered
        response = client.get("/activities")
        data = response.json()
        assert email not in data["Tennis Club"]["participants"]
