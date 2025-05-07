import torch
from PIL import Image
from app.models_code.pytorch_fer2013 import FER2013PytorchModel

def test_pytorch_model_load():
    model = FER2013PytorchModel()
    model.load_model()
    assert model.model is not None
    assert model.model_path.endswith(".pth")

def test_pytorch_model_preprocess():
    model = FER2013PytorchModel()
    image = Image.new("L", (100, 100)) 
    processed_image = model.preprocess(image)
    
    assert processed_image.shape == (1, 1, 48, 48)
    assert isinstance(processed_image, torch.Tensor)

def test_pytorch_model_predict():
    model = FER2013PytorchModel()
    model.load_model()
    dummy_input = torch.rand(1, 1, 48, 48)
    predicted_class, confidence = model.predict(dummy_input)
    
    assert isinstance(predicted_class, int)
    assert isinstance(confidence, float)
