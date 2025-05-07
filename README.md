# Emotion Recognition App 😄😢😠

A cross-platform desktop app that uses deep learning to recognize emotions from facial images or video using 8 models (TensorFlow + PyTorch). Developed with React + Electron + FastAPI.

## 👨‍💻 Tech Stack

- Frontend: ReactJS, Electron, FaceAPI.js
- Backend: Python, FastAPI
- ML: TensorFlow, PyTorch (VGG16 models)

## 💡 Features

- Real-time webcam-based emotion recognition
- Upload image/video for analysis
- Compare 8 emotion models
- Fully local app (no cloud required)

## 🧠 Datasets Used

- FER2013
- KDEF
- NHFI
- Mixed Dataset

## 🧪 Model Training

Each dataset was used to train two models (TensorFlow + PyTorch). A two-phase transfer learning strategy was used with VGG16 as the base model.

## 🚀 How to Run It

### Backend
```bash
cd Backend
pip install -r requirements.txt
uvicorn app.main:app --reload
