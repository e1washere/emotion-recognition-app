import os
import shutil

def copy_folder(destination_path, new_folder_name, source_folder_path):
    os.makedirs(destination_path, exist_ok=True)

    new_folder_path = os.path.join(destination_path, new_folder_name)

    shutil.copytree(source_folder_path, new_folder_path, dirs_exist_ok=False)

