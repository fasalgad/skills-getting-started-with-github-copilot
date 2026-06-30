from urllib.parse import quote

from src.app import activities


def test_unregister_success(client):
    activity_name = "Chess Club"
    existing_email = activities[activity_name]["participants"][0]

    response = client.delete(
        f"/activities/{quote(activity_name, safe='')}/participants/{quote(existing_email, safe='')}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {existing_email} from {activity_name}"
    assert existing_email not in activities[activity_name]["participants"]


def test_unregister_fails_for_missing_activity(client):
    response = client.delete(
        f"/activities/{quote('Unknown Club', safe='')}/participants/{quote('new.student@mergington.edu', safe='')}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_fails_for_student_not_registered(client):
    activity_name = "Chess Club"
    missing_email = "not.registered@mergington.edu"

    response = client.delete(
        f"/activities/{quote(activity_name, safe='')}/participants/{quote(missing_email, safe='')}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"
