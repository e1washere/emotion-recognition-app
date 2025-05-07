from PreprocessSet import preprocess_set

train_path = './Mixed/train'
test_path = './Mixed/test'


train_images_array_path = './Mixed/train_images.npy'
test_images_array_path = './Mixed/test_images.npy'

train_labels_array_path = './Mixed/train_labels.npy'
test_labels_array_path = './Mixed/test_labels.npy'
image_size = (224, 224)
emotions = ['afraid', 'angry', 'disgusted', 'happy', 'neutral', 'sad', 'surprised']

print(f"Preprocessing train set")
preprocess_set(train_images_array_path, train_labels_array_path, train_path, image_size, emotions)

print(f"Preprocessing test set")
preprocess_set(test_images_array_path, test_labels_array_path, test_path, image_size, emotions)
