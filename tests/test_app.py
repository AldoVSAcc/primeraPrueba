from urllib.parse import quote


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_keys = {"Chess Club", "Programming Class", "Gym Class"}

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_keys.issubset(data.keys())
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    path = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(path, params={"email": email})
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["message"] == f"Signed up {email} for {activity_name}"

    refreshed = client.get("/activities").json()
    assert email in refreshed[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    path = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(path, params={"email": email})
    data = response.json()

    # Assert
    assert response.status_code == 400
    assert data["detail"] == "Student already signed up for this activity"


def test_remove_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    path = f"/activities/{quote(activity_name)}/participants"

    # Act
    response = client.delete(path, params={"email": email})
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["message"] == f"Removed {email} from {activity_name}"

    refreshed = client.get("/activities").json()
    assert email not in refreshed[activity_name]["participants"]


def test_remove_nonexistent_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "missing.student@mergington.edu"
    path = f"/activities/{quote(activity_name)}/participants"

    # Act
    response = client.delete(path, params={"email": email})
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert data["detail"] == "Participant not found"
