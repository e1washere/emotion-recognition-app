import os
import numpy as np
from PIL import Image

def preprocess_set(images_array_path, labels_array_path, dataset_path, image_size, emotions):

    emotion_to_label = {emotion: idx for idx, emotion in enumerate(emotions)}

    image_list = []
    label_list = []

    for emotion in emotions:
        emotion_folder = os.path.join(dataset_path, emotion)
        label = emotion_to_label[emotion]
        for filename in os.listdir(emotion_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_path = os.path.join(emotion_folder, filename)

                img = Image.open(image_path)

                img = img.convert('L')

                if img.size != image_size:
                    img = img.resize(image_size)

                img_array = np.array(img, dtype=np.float32)

                img_array /= 255.0

                img_array = img_array.reshape(image_size[0], image_size[1], 1)
                
                image_list.append(img_array)
                label_list.append(label)

        print(f"Processed {emotion}")

    images = np.array(image_list)
    labels = np.array(label_list)

    np.save(images_array_path, images)
    np.save(labels_array_path, labels)

    print(f"Total number of images: {images.shape[0]}")
    print(f"Images array shape: {images.shape}")
    print(f"Labels array shape: {labels.shape}")
    print("\nLabel mapping:")
    for emotion, idx in emotion_to_label.items():
        print(f"Label {idx}: {emotion}")

