emotion_labels_8 = {
    0: 'afraid',
    1: 'angry',
    2: 'disgusted',
    3: 'happy',
    4: 'neutral',
    5: 'sad',
    6: 'surprised',
    7: 'contempt'
}

def get_emotion_label_8(class_idx):
    print(f"{class_idx} class number")
    return emotion_labels_8.get(class_idx, 'Unknown')