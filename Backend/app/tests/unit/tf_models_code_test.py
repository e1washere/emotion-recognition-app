import numpy as np
from PIL import Image
from app.models_code.tf_fer2013 import FER2013TFModel

def test_tf_model_load():
    model = FER2013TFModel()
    model.load_model()
    assert model.model is not None

def test_tf_model_preprocess():
    model = FER2013TFModel()
    image = Image.new("L", (100, 100)) 
    processed_image = model.preprocess(image)
    
    assert processed_image.shape == (1, 48, 48, 1)
    assert processed_image.dtype == np.float32

def test_tf_model_predict():
    model = FER2013TFModel()
    model.load_model()
    dummy_input = np.random.rand(1, 48, 48, 1).astype(np.float32)
    predicted_class, confidence = model.predict(dummy_input)
    
    predicted_class = int(predicted_class)
    
    assert isinstance(predicted_class, int)
    assert isinstance(confidence, float)
