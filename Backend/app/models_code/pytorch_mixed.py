import os
import sys
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from app.models_code.pytorch_base_class import PytorchBaseClass

class EmotionCNN(nn.Module):
    def __init__(self, num_classes):
        super(EmotionCNN, self).__init__()
        vgg16_full = models.vgg16()
        self.features = vgg16_full.features
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc1 = nn.Linear(512, 256)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(256, num_classes)

    def forward(self, x):
        x = self.features(x)
        x = self.pool(x)  
        x = torch.flatten(x, 1)  
        x = F.relu(self.fc1(x))  
        x = self.dropout(x)
        x = self.fc2(x) 
        return x

class MixedPytorchModel(PytorchBaseClass):
    def __init__(self):
        super().__init__()
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        self.model_path = os.path.join(base_path, 'app/models/emotion_model_pytorch_mixed.pth')

        IMAGENET_MEAN = [0.485, 0.456, 0.406]
        IMAGENET_STD = [0.229, 0.224, 0.225]

        self.preprocess_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ])

    def create_model(self):
        return EmotionCNN(num_classes=7)
