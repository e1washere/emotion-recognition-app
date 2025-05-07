import os
from PIL import Image

def zoom_in_images(directory_path, max_count):
    for folder_name in os.listdir(directory_path):
        folder_path = os.path.join(directory_path, folder_name)

        count = sum(1 for filename in os.listdir(folder_path))
        

        for filename in os.listdir(folder_path):
            if count < max_count:
                if '_zoomed' in filename or "_rotated" in filename:
                    continue

                image_path = os.path.join(folder_path, filename)
                image = Image.open(image_path)
                
                width, height = image.size

                zoom_factor = 0.1
                crop_width = int(width * zoom_factor)
                crop_height = int(height * zoom_factor)

                left = crop_width
                top = crop_height
                right = width - crop_width
                bottom = height - crop_height

                zoomed_image = image.crop((left, top, right, bottom)).resize((width, height))

                path, ext = os.path.splitext(image_path)
                zoomed_image_path = f"{path}_zoomed{ext}"

                zoomed_image.save(zoomed_image_path)

                count += 1
            else:
                break
        
        print(f"Processed {folder_name}. Final count in folder: {count}")
            