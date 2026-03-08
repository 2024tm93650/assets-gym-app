import pytest
from app import app, calculate_bmi


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_status_code(client):
    response = client.get("/")
    assert response.status_code == 200


def test_home_returns_json(client):
    response = client.get("/")
    data = response.get_json()
    assert "message" in data
    assert "ACEest Fitness & Gym" in data["message"]


def test_home_has_tagline(client):
    response = client.get("/")
    data = response.get_json()
    assert "tagline" in data
    assert data["status"] == "active"


def test_members_status_code(client):
    response = client.get("/members")
    assert response.status_code == 200


def test_members_returns_json(client):
    response = client.get("/members")
    data = response.get_json()
    assert "members" in data
    assert "total" in data
    assert isinstance(data["members"], list)
    assert data["total"] > 0


def test_get_single_member(client):
    response = client.get("/members/1")
    assert response.status_code == 200


def test_get_member_not_found(client):
    response = client.get("/members/999")
    assert response.status_code == 404


def test_classes_status_code(client):
    response = client.get("/classes")
    assert response.status_code == 200


def test_bmi_normal_weight(client):
    response = client.get("/bmi?weight=70&height=1.75")
    assert response.status_code == 200


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200