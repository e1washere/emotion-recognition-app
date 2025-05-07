import os
from PIL import Image, ImageEnhance

def brighten_images(directory_path, max_count):
    for folder_name in os.listdir(directory_path):
        folder_path = os.path.join(directory_path, folder_name)

        count = sum(1 for filename in os.listdir(folder_path))
        

        for filename in os.listdir(folder_path):
            if count < max_count:
                if '_brightened' in filename or '_darkened' in filename:
                    continue

                image_path = os.path.join(folder_path, filename)
                image = Image.open(image_path)
                enhancer = ImageEnhance.Brightness(image)
                brightened_image = enhancer.enhance(1.1)

                path, ext = os.path.splitext(image_path)
                brightened_image_path = f"{path}_brightened{ext}"

                brightened_image.save(brightened_image_path)

                count += 1
            else:
                break
        
        print(f"Processed {folder_name}. Final count in folder: {count}")
            