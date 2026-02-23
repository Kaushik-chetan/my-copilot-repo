"""
Tests for the activity signup endpoint (POST /activities/{activity_name}/signup).
"""

import pytest


class TestSignup:
    """Tests for signing up students for activities."""

    def test_signup_success(self, client):
        """Verify a student can successfully sign up for an activity."""
        response = client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
        assert "Basketball Team" in data["message"]

    def test_signup_updates_participants_list(self, client):
        """Verify signup actually adds student to participants list."""
        # Sign up a new student
        client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        
        # Verify in activities list
        response = client.get("/activities")
        data = response.json()
        assert "newstudent@mergington.edu" in data["Basketball Team"]["participants"]

    def test_signup_multiple_students_same_activity(self, client):
        """Verify multiple students can sign up for the same activity."""
        # Sign up first student
        response1 = client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": "student1@mergington.edu"}
        )
        assert response1.status_code == 200
        
        # Sign up second student
        response2 = client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": "student2@mergington.edu"}
        )
        assert response2.status_code == 200
        
        # Verify both are in list
        response = client.get("/activities")
        data = response.json()
        assert "student1@mergington.edu" in data["Basketball Team"]["participants"]
        assert "student2@mergington.edu" in data["Basketball Team"]["participants"]
        assert len(data["Basketball Team"]["participants"]) == 2

    def test_signup_activity_not_found(self, client):
        """Verify signup returns 404 for non-existent activity."""
        response = client.post(
            "/activities/Nonexistent%20Activity/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_already_registered(self, client):
        """Verify student cannot sign up twice for the same activity."""
        email = "newstudent@mergington.edu"
        
        # First signup should succeed
        response1 = client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Second signup should fail
        response2 = client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": email}
        )
        assert response2.status_code == 400
        data = response2.json()
        assert "already signed up" in data["detail"]

    def test_signup_already_registered_different_activity(self, client):
        """Verify student can sign up for different activities."""
        email = "newstudent@mergington.edu"
        
        # Sign up for Basketball Team
        response1 = client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Can also sign up for Tennis Club (different activity)
        response2 = client.post(
            "/activities/Tennis%20Club/signup",
            params={"email": email}
        )
        assert response2.status_code == 200
        
        # Verify both signups
        response = client.get("/activities")
        data = response.json()
        assert email in data["Basketball Team"]["participants"]
        assert email in data["Tennis Club"]["participants"]

    def test_signup_existing_participant(self, client):
        """Verify existing participant cannot sign up again."""
        # Michael is already in Chess Club
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_response_format(self, client):
        """Verify signup response has correct format."""
        response = client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": "student@mergington.edu"}
        )
        data = response.json()
        assert "message" in data
        assert isinstance(data["message"], str)
        assert len(data["message"]) > 0

    def test_signup_with_special_characters_in_email(self, client):
        """Verify signup works with various email formats."""
        # Email with plus sign (common for testing)
        response = client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": "student+test@mergington.edu"}
        )
        assert response.status_code == 200

    def test_signup_case_sensitivity_email(self, client):
        """Verify email signup is case-sensitive."""
        email_lower = "newstudent@mergington.edu"
        email_upper = "NewStudent@mergington.edu"
        
        # Sign up with lowercase
        response1 = client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": email_lower}
        )
        assert response1.status_code == 200
        
        # Should be able to sign up with different case (case-sensitive)
        response2 = client.post(
            "/activities/Tennis%20Club/signup",
            params={"email": email_upper}
        )
        assert response2.status_code == 200

    def test_signup_activity_name_case_sensitivity(self, client):
        """Verify activity name lookup is case-sensitive."""
        # Wrong case should not find activity
        response = client.post(
            "/activities/basketball%20team/signup",  # lowercase 'b'
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
