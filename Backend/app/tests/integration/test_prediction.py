import base64
import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict_emotion_valid_data():
    test_image_path = os.path.join(
        os.path.dirname(__file__),
        "test_images",
        "face_image.jpg"
    )

    with open(test_image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "image_data": image_data,
        "model_name": "fer2013_pytorch"
    }

    response = client.post("/api/predict_emotion", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert "emotion" in data
    assert "confidence" in data
    assert data["emotion"] in [
        "afraid", "angry", "disgusted", "happy",
        "neutral", "sad", "surprised", "contempt"
    ]

def test_predict_emotion_invalid_model():
    test_image_path = os.path.join(
        os.path.dirname(__file__),
        "test_images",
        "face_image.jpg"
    )
    with open(test_image_path, "rb") as f:
        dummy_image_data = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "image_data": dummy_image_data,
        "model_name": "this_model_does_not_exist"
    }

    response = client.post("/api/predict_emotion", json=payload)
    assert response.status_code == 400
    assert "Model" in response.json()["detail"]

def test_predict_emotion_bad_image_data():
    payload = {
        "image_data": "notReallyBase64!!??",
        "model_name": "fer2013_pytorch"
    }

    response = client.post("/api/predict_emotion", json=payload)
    assert response.status_code == 400
    assert "Invalid image data." in response.json()["detail"]
