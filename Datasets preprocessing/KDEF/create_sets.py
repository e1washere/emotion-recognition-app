from KDEF.KDEF_sort import kdef_sort
from CreateTestSet import create_test_set
from CopyToMixedSet import copy_to_mixed_set
from PreprocessSet import preprocess_set

directory_path = './KDEF'

original_path = './KDEF/KDEF'

train_path = './KDEF/KDEF_train'
train_path_with_directory = './KDEF/KDEF_train'

test_path_with_directory = './KDEF/KDEF_test'


print(f"Sorting KDEF set")
kdef_sort(original_path, train_path)

print(f"Creating test set")
create_test_set(train_path_with_directory, test_path_with_directory, 70)

mixed_train_path = './Mixed/train'
mixed_test_path = './Mixed/test'
print(f"Copying images to train mixed set")
copy_to_mixed_set(train_path_with_directory, 630, mixed_train_path)
print(f"Copying images to test mixed set")
copy_to_mixed_set(test_path_with_directory, 70, mixed_test_path)


train_images_array_path = './KDEF/train_images.npy'
test_images_array_path = './KDEF/test_images.npy'

train_labels_array_path = './KDEF/train_labels.npy'
test_labels_array_path = './KDEF/test_labels.npy'

image_size = (224, 224)
emotions = ['afraid', 'angry', 'disgusted', 'happy', 'neutral', 'sad', 'surprised']
print(f"Preprcoessing train set")
preprocess_set(train_images_array_path, train_labels_array_path, train_path_with_directory, image_size, emotions)
print(f"Preprcoessing test set")
preprocess_set(test_images_array_path, test_labels_array_path, test_path_with_directory, image_size, emotions)