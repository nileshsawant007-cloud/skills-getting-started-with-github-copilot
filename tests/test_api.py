from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_contains_known_activity():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Basketball" in data
    assert isinstance(data["Basketball"], dict)


def test_signup_and_unregister_flow():
    activity = "Basketball"
    email = "test_student@example.com"

    # Ensure not present initially
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    participants = data[activity]["participants"]
    if email in participants:
        # remove if left over from prior runs
        client.delete(f"/activities/{activity}/unregister?email={email}")

    # Sign up
    signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup.status_code == 200
    assert "Signed up" in signup.json().get("message", "")

    # Verify present
    resp = client.get("/activities")
    data = resp.json()
    assert email in data[activity]["participants"]

    # Unregister
    unreg = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert unreg.status_code == 200
    assert "Unregistered" in unreg.json().get("message", "")

    # Verify removed
    resp = client.get("/activities")
    data = resp.json()
    assert email not in data[activity]["participants"]
