from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_competition():
    response = client.post(
        "/competitions",
        json={
            "name": "Premier League",
            "country": "England",
            "sport": "Football",
            "season": "2025/26",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Premier League"
    assert data["country"] == "England"
    assert data["sport"] == "Football"
    assert data["season"] == "2025/26"
    assert "id" in data


def test_list_competitions():
    response = client.get("/competitions")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_competition_not_found():
    fake_id = "11111111-1111-1111-1111-111111111111"

    response = client.get(f"/competitions/{fake_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Competition not found"