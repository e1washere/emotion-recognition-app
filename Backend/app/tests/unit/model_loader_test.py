from app.utils.model_loader import preload_models, get_model, MODEL_CACHE
from unittest.mock import MagicMock, patch

@patch("app.utils.model_loader.MODEL_CLASSES", {"test_model": MagicMock()})
def test_preload_models():
    preload_models()
    assert "test_model" in MODEL_CACHE
    assert MODEL_CACHE["test_model"].load_model.called

@patch("app.utils.model_loader.MODEL_CACHE", {"test_model": MagicMock()})
def test_get_model_valid():
    model = get_model("test_model")
    assert model is not None

def test_get_model_invalid():
    try:
        get_model("invalid_model")
    except ValueError as e:
        assert "Model 'invalid_model' not found." in str(e)
