from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_create_review():
    response = client.post(
        "/reviews/",
        json={
            "customer_id": 1,
            "menu_item_id": 1,
            "review_text": "Excellent",
            "score": 5
        }
    )

    assert response.status_code == 200
    assert response.json()["score"] == 5


def test_score_validation():
    response = client.post(
        "/reviews/",
        json={
            "customer_id": 1,
            "menu_item_id": 1,
            "review_text": "Invalid",
            "score": 10
        }
    )

    assert response.status_code == 422


def test_get_reviews():
    response = client.get("/reviews/")
    assert response.status_code in [200, 404]