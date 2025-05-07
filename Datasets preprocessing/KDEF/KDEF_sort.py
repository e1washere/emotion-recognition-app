import os
import shutil
import re

expression_mapping = {
    'AF': 'afraid',
    'AN': 'angry',
    'DI': 'disgusted',
    'HA': 'happy',
    'NE': 'neutral',
    'SA': 'sad',
    'SU': 'surprised'
}

def get_expression_from_filename(filename):
    match = re.match(r"^.{4}(.{2}).*\.JPG$", filename) 
    return match.group(1) if match else None

def kdef_sort(original_folder_path, destination_folder_path):
    os.makedirs(destination_folder_path, exist_ok=True)

    i = 1

    for folder_name in os.listdir(original_folder_path):
        folder_path = os.path.join(original_folder_path, folder_name)

        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                if filename.endswith('.JPG'):
                    expression_code = get_expression_from_filename(filename)

                    if expression_code and expression_code in expression_mapping:
                        target_folder_name = expression_mapping[expression_code]
                        target_folder_path = os.path.join(destination_folder_path, target_folder_name)

                        os.makedirs(target_folder_path, exist_ok=True)

                        source_file_path = os.path.join(folder_path, filename)
                        destination_file_path = os.path.join(target_folder_path, filename)

                        shutil.copy(source_file_path, destination_file_path)

        print(f"{i}. Folder {folder_name} processed")
        i += 1
