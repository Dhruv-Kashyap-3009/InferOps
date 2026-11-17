from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_valid():
    payload = {"sepal_length": 5.1, "sepal_width": 3.5,
               "petal_length": 1.4, "petal_width": 0.2}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert response.json() == {"prediction": "setosa"}


def test_predict_invalid():
    # A negative measurement must be rejected by validation
    payload = {"sepal_length": -1, "sepal_width": 3.5,
               "petal_length": 1.4, "petal_width": 0.2}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Iris classifier" in response.text
