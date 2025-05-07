import os
from PIL import Image 


def mirror_images(directory_path, max_count):
    for folder_name in os.listdir(directory_path):
        folder_path = os.path.join(directory_path, folder_name)

        count = sum(1 for filename in os.listdir(folder_path))

        for filename in os.listdir(folder_path):
            if count < max_count:
                if '_mirrored' in filename:
                    continue

                image_path = os.path.join(folder_path, filename)
                image = Image.open(image_path)
                mirrored_image = image.transpose(Image.FLIP_LEFT_RIGHT)

                path, ext = os.path.splitext(image_path)
                mirrored_image_path = f"{path}_mirrored{ext}"

                mirrored_image.save(mirrored_image_path)

                count += 1
            else:
                break
        
        print(f"Processed {folder_name}. Final count in folder: {count}")
        