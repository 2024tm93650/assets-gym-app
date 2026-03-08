"""Unit tests for ACEest Fitness & Gym Flask application."""

import pytest
from app import app, calculate_bmi


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ---- Home endpoint tests ----

def test_home_status_code(client):
    """Test that the home route returns status 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_home_returns_json(client):
    """Test that the home route returns valid JSON with welcome message."""
    response = client.get("/")
    data = response.get_json()
    assert "message" in data
    assert "ACEest Fitness & Gym" in data["message"]


def test_home_has_tagline(client):
    """Test that the home response includes a tagline."""
    response = client.get("/")
    data = response.get_json()
    assert "tagline" in data
    assert data["status"] == "active"


# ---- Members endpoint tests ----

def test_members_status_code(client):
    """Test that the /members endpoint returns status 200."""
    response = client.get("/members")
    assert response.status_code == 200


def test_members_returns_json(client):
    """Test that the /members endpoint returns JSON with member data."""
    response = client.get("/members")
    data = response.get_json()
    assert "members" in data
    assert "total" in data
    assert isinstance(data["members"], list)
    assert data["total"] > 0


def test_members_data_structure(client):
    """Test that each member has the expected fields."""
    response = client.get("/members")
    data = response.get_json()
    for member in data["members"]:
        assert "id" in member
        assert "name" in member
        assert "membership" in member
        assert "age" in member


def test_get_single_member(client):
    """Test fetching a single member by ID."""
    response = client.get("/members/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Alice Johnson"
    assert data["membership"] == "Gold"


def test_get_member_not_found(client):
    """Test 404 when member ID does not exist."""
    response = client.get("/members/999")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


# ---- Classes endpoint tests ----

def test_classes_status_code(client):
    """Test that the /classes endpoint returns status 200."""
    response = client.get("/classes")
    assert response.status_code == 200


def test_classes_returns_json(client):
    """Test that the /classes endpoint returns class data."""
    response = client.get("/classes")
    data = response.get_json()
    assert "classes" in data
    assert "total" in data
    assert isinstance(data["classes"], list)
    assert data["total"] > 0


def test_classes_data_structure(client):
    """Test that each class has the expected fields."""
    response = client.get("/classes")
    data = response.get_json()
    for gym_class in data["classes"]:
        assert "id" in gym_class
        assert "name" in gym_class
        assert "trainer" in gym_class
        assert "schedule" in gym_class


# ---- BMI endpoint tests ----

def test_bmi_normal_weight(client):
    """Test BMI calculation for a normal weight person."""
    response = client.get("/bmi?weight=70&height=1.75")
    assert response.status_code == 200
    data = response.get_json()
    assert "bmi" in data
    assert "category" in data
    assert data["category"] == "Normal weight"


def test_bmi_overweight(client):
    """Test BMI calculation for an overweight person."""
    response = client.get("/bmi?weight=90&height=1.75")
    assert response.status_code == 200
    data = response.get_json()
    assert data["category"] == "Overweight"


def test_bmi_missing_params(client):
    """Test BMI endpoint returns 400 with missing parameters."""
    response = client.get("/bmi")
    assert response.status_code == 400


def test_bmi_invalid_params(client):
    """Test BMI endpoint returns 400 with invalid values."""
    response = client.get("/bmi?weight=abc&height=1.75")
    assert response.status_code == 400


# ---- BMI helper function tests ----

def test_calculate_bmi_underweight():
    """Test calculate_bmi returns Underweight for low BMI."""
    result = calculate_bmi(45, 1.75)
    assert result["category"] == "Underweight"


def test_calculate_bmi_obese():
    """Test calculate_bmi returns Obese for high BMI."""
    result = calculate_bmi(120, 1.75)
    assert result["category"] == "Obese"


def test_calculate_bmi_invalid_input():
    """Test calculate_bmi returns error for non-positive values."""
    result = calculate_bmi(-10, 1.75)
    assert "error" in result
    result = calculate_bmi(70, 0)
    assert "error" in result


# ---- Health endpoint tests ----

def test_health_endpoint(client):
    """Test that the /health endpoint returns status 200 and healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
