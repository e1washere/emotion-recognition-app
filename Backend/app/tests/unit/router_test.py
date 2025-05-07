from fastapi import HTTPException
from app.routers.prediction import predict_emotion_endpoint, ImagePayload
from unittest.mock import patch, MagicMock
import pytest
import base64
from io import BytesIO
from PIL import Image

def generate_valid_base64_image():
    image = Image.new("RGB", (48, 48), color="white")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

@pytest.mark.asyncio
@patch("app.routers.prediction.get_model")
async def test_predict_emotion_valid(mock_get_model):
    mock_model = MagicMock()
    mock_model.preprocess.return_value = "preprocessed_image"
    mock_model.predict.return_value = (3, 0.95) 
    mock_get_model.return_value = mock_model

    valid_image_data = generate_valid_base64_image()
    payload = ImagePayload(image_data=valid_image_data, model_name="fer2013_pytorch")
    
    response = await predict_emotion_endpoint(payload)
    
    assert response.emotion == "happy"
    assert response.confidence == 0.95

@pytest.mark.asyncio
@patch("app.routers.prediction.get_model")
async def test_predict_emotion_invalid_model(mock_get_model):
    mock_get_model.side_effect = ValueError("Model 'invalid_model' not found.")

    valid_image_data = generate_valid_base64_image()
    payload = ImagePayload(image_data=valid_image_data, model_name="invalid_model")
    
    with pytest.raises(HTTPException) as exc_info:
        await predict_emotion_endpoint(payload)
    
    assert exc_info.value.status_code == 400
    assert "Model" in str(exc_info.value.detail)

@pytest.mark.asyncio
async def test_predict_emotion_bad_image_data():
    payload = ImagePayload(image_data="not_base64", model_name="fer2013_pytorch")
    
    with pytest.raises(HTTPException) as exc_info:
        await predict_emotion_endpoint(payload)
    
    assert exc_info.value.status_code == 400
    assert "Invalid image data." in str(exc_info.value.detail)
