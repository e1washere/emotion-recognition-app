import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import models
from torchvision.models import VGG16_Weights
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

data_dir = "/kaggle/input/mixed-npys"

train_images = np.load(os.path.join(data_dir, "train_images.npy"))  # (N,224,224,1)
train_labels = np.load(os.path.join(data_dir, "train_labels.npy"))  # (N,)
test_images  = np.load(os.path.join(data_dir, "test_images.npy"))   # (M,224,224,1)
test_labels  = np.load(os.path.join(data_dir, "test_labels.npy"))   # (M,)

num_classes = 7  # afraid, angry, disgusted, happy, neutral, sad, surprised
print(f"Train images: {train_images.shape}, Train labels: {train_labels.shape}")
print(f"Test images: {test_images.shape}, Test labels: {test_labels.shape}")
print(f"Number of classes: {num_classes}")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# 0=afraid,1=angry,2=disgusted,3=happy,4=neutral,5=sad,6=surprised

IMAGENET_MEAN = torch.tensor([0.485, 0.456, 0.406]).view(3,1,1)
IMAGENET_STD  = torch.tensor([0.229, 0.224, 0.225]).view(3,1,1)

class MixedDataset(Dataset):
    def __init__(self, images, labels):
        self.images = images
        self.labels = labels

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img = self.images[idx]  # shape (224,224,1 or 3)
        label = self.labels[idx]

        # Convert to float32
        img_tensor = torch.from_numpy(img).float()

        # If 1-channel, replicate
        if img_tensor.shape[-1] == 1:
            img_tensor = img_tensor.permute(2,0,1)
            img_tensor = img_tensor.repeat(3,1,1)
        else:
            img_tensor = img_tensor.permute(2,0,1)

        # Normalize
        img_tensor = (img_tensor - IMAGENET_MEAN) / IMAGENET_STD
        return img_tensor, label

train_dataset = MixedDataset(train_images, train_labels)
test_dataset  = MixedDataset(test_images,  test_labels)

batch_size = 8
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True,  num_workers=2, pin_memory=True)
test_loader  = DataLoader(test_dataset,  batch_size=batch_size, shuffle=False, num_workers=2, pin_memory=True)

vgg16_full = models.vgg16(weights=VGG16_Weights.IMAGENET1K_V1)

class VGG16CustomHead(nn.Module):
    def __init__(self, vgg16_full, num_classes):
        super().__init__()
        self.features = vgg16_full.features
        self.pool = nn.AdaptiveAvgPool2d((1,1))
        self.fc1 = nn.Linear(512, 256)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(256, num_classes)

    def forward(self, x):
        x = self.features(x)
        x = self.pool(x)               # (N,512,1,1)
        x = torch.flatten(x, 1)        # (N,512)
        x = F.relu(self.fc1(x))        # (N,256)
        x = self.dropout(x)
        x = self.fc2(x)                # (N,num_classes)
        return x

model = VGG16CustomHead(vgg16_full, num_classes).to(device)

best_model_path = "best_mixed_pt.pth"
best_val_acc = 0.0

def save_best_model_if_needed(val_acc):
    global best_val_acc
    if val_acc >= 0.60 and val_acc > best_val_acc:
        torch.save(model.state_dict(), best_model_path)
        print(f"[Saving best] val_acc={val_acc:.4f} > best_val_acc={best_val_acc:.4f}")
        best_val_acc = val_acc

criterion = nn.CrossEntropyLoss()

def evaluate_accuracy(loader):
    model.eval()
    correct = 0
    total   = 0
    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total   += labels.size(0)
    return correct / total

for param in model.features.parameters():
    param.requires_grad = False

optimizer = optim.Adam([p for p in model.parameters() if p.requires_grad], lr=1e-3)

print("=== PHASE 1: (5 epochs) freeze conv base ===")
for epoch in range(5):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    val_acc = evaluate_accuracy(test_loader)
    avg_loss = running_loss / len(train_loader)
    print(f"Epoch [{epoch+1}/5] Loss: {avg_loss:.4f}, Val_Acc: {val_acc:.4f}")
    save_best_model_if_needed(val_acc)

for param in model.features.parameters():
    param.requires_grad = True

optimizer = optim.Adam(model.parameters(), lr=1e-5)

print("=== PHASE 2: (20 epochs) unfreeze entire base ===")
for epoch in range(20):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    val_acc = evaluate_accuracy(test_loader)
    avg_loss = running_loss / len(train_loader)
    print(f"Epoch [{epoch+1}/20] Loss: {avg_loss:.4f}, Val_Acc: {val_acc:.4f}")
    save_best_model_if_needed(val_acc)

print("\n=== Loading best checkpoint from disk ===")
model.load_state_dict(torch.load(best_model_path))

final_acc = evaluate_accuracy(test_loader)
print(f"[BEST MODEL] Test Accuracy: {final_acc*100:.2f}%")

# Collect predictions & labels
all_preds = []
all_labels = []
model.eval()
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, preds = torch.max(outputs, 1)
        all_preds.append(preds.cpu().numpy())
        all_labels.append(labels.cpu().numpy())

all_preds  = np.concatenate(all_preds)
all_labels = np.concatenate(all_labels)

# Classification report
emotion_names = ["afraid","angry","disgusted","happy","neutral","sad","surprised"]
report = classification_report(all_labels, all_preds, target_names=emotion_names)
print(report)

with open("vgg16_mixed_pt_report.txt", "w") as f:
    f.write(report)

# Confusion Matrix (%)
cm = confusion_matrix(all_labels, all_preds).astype(np.float32)
row_sums = cm.sum(axis=1, keepdims=True)
cm_perc = (cm / row_sums) * 100.0

print("Confusion Matrix (%):")
print(cm_perc)

plt.figure(figsize=(7,6))
sns.heatmap(cm_perc, annot=True, fmt=".2f", cmap="Blues",
            xticklabels=emotion_names, yticklabels=emotion_names)
plt.title("Mixed (PyTorch) - Confusion Matrix (%) [BEST MODEL]")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.savefig("confusion_matrix_mixed_pt.png", dpi=300, bbox_inches='tight')
plt.show()

print("All done! Best model: best_mixed_pt.pth")