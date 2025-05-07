import os
import shutil

def divide_test_set(original_directory_path, new_directory_path):

    os.makedirs(new_directory_path, exist_ok=True)

    for folder_name in os.listdir(original_directory_path):
        folder_path = os.path.join(original_directory_path, folder_name)
        new_folder_path = os.path.join(new_directory_path, folder_name)

        os.makedirs(new_folder_path, exist_ok=True)

        copied_files = 0 

        for filename in os.listdir(folder_path):
            if 'PrivateTest' in filename:
                image_path = os.path.join(folder_path, filename)
                new_image_path = os.path.join(new_folder_path, filename)
                
                try:
                    shutil.copy(image_path, new_image_path)
                    copied_files += 1  
                except Exception as e:
                    print(f"Error copying {image_path}: {e}")

        print(f"Processed folder '{folder_name}': {copied_files} files copied.")


