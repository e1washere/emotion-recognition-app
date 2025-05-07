emotion_labels_7 = {
    0: 'afraid',
    1: 'angry',
    2: 'disgusted',
    3: 'happy',
    4: 'neutral',
    5: 'sad',
    6: 'surprised'
}

def get_emotion_label_7(class_idx):
    return emotion_labels_7.get(class_idx, 'Unknown')