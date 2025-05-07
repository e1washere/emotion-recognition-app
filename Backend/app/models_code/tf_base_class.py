import tensorflow as tf
import numpy as np
from PIL import Image

class TFBaseClass:

    def __init__(self):
        self.model = None
        self.model_path = None
        self.input_height = 224
        self.input_width = 224
        self.num_channels = 3 

    def load_model(self):
        if not self.model_path:
            raise ValueError("No model_path defined in subclass.")
        self.model = tf.keras.models.load_model(self.model_path)

    def preprocess(self, image: Image.Image):
        image = image.resize((self.input_height, self.input_width))
        image_array = np.array(image).astype('float32') / 255.0

        if self.num_channels == 3 and image_array.ndim == 2:  
            image_array = np.stack([image_array] * 3, axis=-1)

        image_array -= [0.485, 0.456, 0.406]
        image_array /= [0.229, 0.224, 0.225]

        image_array = np.expand_dims(image_array, axis=0)
        return image_array

    def predict(self, image_array: np.ndarray):
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")

        predictions = self.model.predict(image_array)
        predicted_class = np.argmax(predictions, axis=1)[0]
        confidence = predictions[0][predicted_class]
        return predicted_class, float(confidence)
