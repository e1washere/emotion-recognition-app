import os
from PIL import Image 


def zooming_in(image):
    width, height = image.size

    zoom_factor = 0.1
    crop_width = int(width * zoom_factor)
    crop_height = int(height * zoom_factor)

    left = crop_width
    top = crop_height
    right = width - crop_width
    bottom = height - crop_height

    return image.crop((left, top, right, bottom)).resize((width, height))


def rotate_images(directory_path, max_count):
    for folder_name in os.listdir(directory_path):
        folder_path = os.path.join(directory_path, folder_name)

        count = sum(1 for filename in os.listdir(folder_path))
        
        for filename in os.listdir(folder_path):
            if count < max_count:
                if '_rotated' in filename:
                    continue

                image_path = os.path.join(folder_path, filename)
                image = Image.open(image_path)
                rotated_left_image = image.rotate(10)
                rotated_right_image = image.rotate(-10)

                rotated_left_image = zooming_in(rotated_left_image)
                rotated_right_image = zooming_in(rotated_right_image)


                
                path, ext = os.path.splitext(image_path)
                rotated_left_image_path = f"{path}_rotated_left{ext}"
                rotated_right_image_path = f"{path}_rotated_right{ext}"


                rotated_left_image.save(rotated_left_image_path)
                rotated_right_image.save(rotated_right_image_path)


                count += 2
            else:
                break
            
        print(f"Processed {folder_name}. Final count in folder: {count}")
        