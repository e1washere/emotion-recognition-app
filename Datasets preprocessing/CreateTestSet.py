import os
import shutil
import random


def create_test_set(original_directory_path, new_directory_path, number_of_images):
    for folder_name in os.listdir(original_directory_path):
        folder_path = os.path.join(original_directory_path, folder_name)
        new_folder_path = os.path.join(new_directory_path, folder_name)
        
        os.makedirs(new_folder_path, exist_ok=True)

        files = os.listdir(folder_path)

        file_paths = [os.path.join(folder_path, f) for f in files]

        random_files = random.sample(file_paths, number_of_images)

        for file_path in random_files:
            shutil.move(file_path, new_folder_path)
        
        print(f"Processed {folder_name}")
