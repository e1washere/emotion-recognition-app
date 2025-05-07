from FER2013.DivideTestSet import divide_test_set
from CopyFolder import copy_folder
from MirrorImages import mirror_images
from RotateImages import rotate_images
from ZoomImages import zoom_in_images
from BrightenImages import brighten_images
from DarkenImages import darken_images
from CopyToMixedSet import copy_to_mixed_set
from PreprocessSet import preprocess_set

directory_path = './FER2013'

original_train_path = './FER2013/train'
original_test_path = './FER2013/test'

divided_test_set_path = './FER2013/test_divided'

uniform_train_set_path = './FER2013/train_uniform'
uniform_test_set_path = './FER2013/test_uniform'

print(f"Dividing test set")
divide_test_set(original_test_path, divided_test_set_path)


print(f"Creating a copy of the train set named \"train_uniform\"")
copy_folder(directory_path, "train_uniform", original_train_path)
print(f"Creating a copy of the test set named \"test_uniform\"")
copy_folder(directory_path, "test_uniform", divided_test_set_path)


print(f"Mirroring images in train set")
mirror_images(uniform_train_set_path, 7215)
print(f"Mirroring images in test set")
mirror_images(uniform_test_set_path, 879)

print(f"Rotating images in train set")
rotate_images(uniform_train_set_path, 7215)
print(f"Rotating images in test set")
rotate_images(uniform_test_set_path, 879)

print(f"Zooming images in train set")
zoom_in_images(uniform_train_set_path, 7215)
print(f"Zooming images in test set")
zoom_in_images(uniform_test_set_path, 879)

print(f"Brightnening images in train set")
brighten_images(uniform_train_set_path, 7215)
print(f"Brightening images in test set")
brighten_images(uniform_test_set_path, 879)

print(f"Darkening images in train set")
darken_images(uniform_train_set_path, 7215)
print(f"Darkening images in test set")
darken_images(uniform_test_set_path, 879)

mixed_train_path = './Mixed/train'
mixed_test_path = './Mixed/test'
print(f"Copying images to train mixed set")
copy_to_mixed_set(uniform_train_set_path, 1260, mixed_train_path)
print(f"Copying images to test mixed set")
copy_to_mixed_set(uniform_test_set_path, 140, mixed_test_path)


train_images_array_path = './FER2013/train_images.npy'
test_images_array_path = './FER2013/test_images.npy'

train_labels_array_path = './FER2013/train_labels.npy'
test_labels_array_path = './FER2013/test_labels.npy'

image_size = (224, 224)
emotions = ['afraid', 'angry', 'disgusted', 'happy', 'neutral', 'sad', 'surprised']


print(f"Preprcoessing train set")
preprocess_set(train_images_array_path, train_labels_array_path, uniform_train_set_path, image_size, emotions)
print(f"Preprcoessing test set")
preprocess_set(test_images_array_path, test_labels_array_path, uniform_test_set_path, image_size, emotions)