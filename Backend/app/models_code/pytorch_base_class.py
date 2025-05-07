import torch
import torch.nn.functional as F
from torchvision import transforms

class PytorchBaseClass:
    def __init__(self):
        self.model = None
        self.model_path = None

        IMAGENET_MEAN = [0.485, 0.456, 0.406]
        IMAGENET_STD = [0.229, 0.224, 0.225]

        self.preprocess_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ])

    def create_model(self):
        raise NotImplementedError("Subclasses must implement create_model()")

    def load_model(self):
        model = self.create_model()
        if not self.model_path:
            raise ValueError("No model_path defined in subclass.")
        model.load_state_dict(torch.load(self.model_path, map_location=torch.device('cpu')))
        model.eval()
        self.model = model

    def preprocess(self, image):
        image = self.preprocess_transform(image)
        image = image.unsqueeze(0)
        return image

    def predict(self, image):
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")

        with torch.no_grad():
            outputs = self.model(image)
            probs = F.softmax(outputs, dim=1)
            predicted_class = torch.argmax(probs, dim=1).item()
            confidence = probs[0][predicted_class].item()
            return predicted_class, confidence
