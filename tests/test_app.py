import pytest


class TestGetActivities:
    """Test GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, app_with_test_data):
        """
        Arrange: Setup test client
        Act: Make GET request to /activities
        Assert: Verify all activities are returned with correct structure
        """
        # Arrange
        client = app_with_test_data

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 3
        assert "Math Club" in activities
        assert "Art Class" in activities
        assert "Chess Club" in activities

    def test_get_activities_returns_correct_fields(self, app_with_test_data):
        """
        Arrange: Setup test client
        Act: Make GET request to /activities
        Assert: Verify each activity has required fields
        """
        # Arrange
        client = app_with_test_data

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()

        for activity_name, activity_data in activities.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)


class TestSignupForActivity:
    """Test POST /activities/{activity_name}/signup endpoint."""

    def test_signup_new_participant_successfully(self, app_with_test_data):
        """
        Arrange: Setup test client and new participant
        Act: POST signup request for new student
        Assert: Verify student is added to participants
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Math Club"
        email = "frank@test.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "Signed up" in result["message"]
        assert email in result["message"]

        # Verify participant was added
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]

    def test_signup_duplicate_participant_fails(self, app_with_test_data):
        """
        Arrange: Setup test client with existing participant
        Act: Try to signup same participant again
        Assert: Verify 400 error is returned
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Math Club"
        email = "alice@test.edu"  # Already registered

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        result = response.json()
        assert "already signed up" in result["detail"].lower()

    def test_signup_nonexistent_activity_fails(self, app_with_test_data):
        """
        Arrange: Setup test client with non-existent activity
        Act: Try to signup for activity that doesn't exist
        Assert: Verify 404 error is returned
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Nonexistent Activity"
        email = "frank@test.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "not found" in result["detail"].lower()

    def test_signup_participant_count_updates(self, app_with_test_data):
        """
        Arrange: Setup test client and get initial participant count
        Act: Signup new participant
        Assert: Verify participant count increased
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Art Class"
        email = "grace@test.edu"

        initial_activities = client.get("/activities").json()
        initial_count = len(initial_activities[activity_name]["participants"])

        # Act
        client.post(
            f"/activities/{activity_name}/signup?email={email}",
            params={"email": email}
        )

        # Assert
        updated_activities = client.get("/activities").json()
        updated_count = len(updated_activities[activity_name]["participants"])
        assert updated_count == initial_count + 1


class TestUnregisterFromActivity:
    """Test DELETE /activities/{activity_name}/signup endpoint."""

    def test_unregister_existing_participant_successfully(self, app_with_test_data):
        """
        Arrange: Setup test client and existing participant
        Act: DELETE request to unregister participant
        Assert: Verify participant is removed
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Math Club"
        email = "alice@test.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup?email={email}",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "Unregistered" in result["message"]

        # Verify participant was removed
        activities = client.get("/activities").json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_nonexistent_participant_fails(self, app_with_test_data):
        """
        Arrange: Setup test client with participant not in activity
        Act: Try to unregister participant who isn't registered
        Assert: Verify 400 error is returned
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Math Club"
        email = "notregistered@test.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup?email={email}",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        result = response.json()
        assert "not registered" in result["detail"].lower()

    def test_unregister_from_nonexistent_activity_fails(self, app_with_test_data):
        """
        Arrange: Setup test client with non-existent activity
        Act: Try to unregister from activity that doesn't exist
        Assert: Verify 404 error is returned
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Nonexistent Activity"
        email = "alice@test.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup?email={email}",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "not found" in result["detail"].lower()

    def test_unregister_participant_count_updates(self, app_with_test_data):
        """
        Arrange: Setup test client and get initial participant count
        Act: Unregister existing participant
        Assert: Verify participant count decreased
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Math Club"
        email = "alice@test.edu"

        initial_activities = client.get("/activities").json()
        initial_count = len(initial_activities[activity_name]["participants"])

        # Act
        client.delete(
            f"/activities/{activity_name}/signup?email={email}",
            params={"email": email}
        )

        # Assert
        updated_activities = client.get("/activities").json()
        updated_count = len(updated_activities[activity_name]["participants"])
        assert updated_count == initial_count - 1
