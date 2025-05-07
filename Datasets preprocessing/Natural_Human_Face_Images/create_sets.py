from CopyFolder import copy_folder
from MirrorImages import mirror_images
from RotateImages import rotate_images
from ZoomImages import zoom_in_images
from CreateTestSet import create_test_set
from CopyToMixedSet import copy_to_mixed_set
from PreprocessSet import preprocess_set


directory_path = './Natural_Human_Face_Images'
original_path = './Natural_Human_Face_Images/NHFI'

test_path = './Natural_Human_Face_Images/NHFI_test'

train_path = './Natural_Human_Face_Images/NHFI_train'

print(f"Creating a copy of the train set named \"NHFI_train\"")
copy_folder(directory_path, "NHFI_train", original_path)


print(f"Mirroring images")
mirror_images(train_path, 1400)

print(f"Rotating images")
rotate_images(train_path, 1400)

print(f"Zooming images")
zoom_in_images(train_path, 1400)


create_test_set(train_path, test_path, 140)

mixed_train_path = './Mixed/train'
mixed_test_path = './Mixed/test'
print(f"Copying images to train mixed set")
copy_to_mixed_set(train_path, 1260, mixed_train_path)
print(f"Copying images to test mixed set")
copy_to_mixed_set(test_path, 140, mixed_test_path)


train_images_array_path = './Natural_Human_Face_Images/train_images.npy'
test_images_array_path = './Natural_Human_Face_Images/test_images.npy'

train_labels_array_path = './Natural_Human_Face_Images/train_labels.npy'
test_labels_array_path = './Natural_Human_Face_Images/test_labels.npy'

image_size = (224, 224)
emotions = ['afraid', 'angry', 'disgusted', 'happy', 'neutral', 'sad', 'surprised', 'contempt']

print(f"Preprcoessing train set")
preprocess_set(train_images_array_path, train_labels_array_path, train_path, image_size, emotions)
print(f"Preprcoessing test set")
preprocess_set(test_images_array_path, test_labels_array_path, test_path, image_size, emotions)