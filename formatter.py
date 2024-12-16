'''
This script:
1. Changes image names in the `/images` folder into a hash.
2. Determines the aspect ratio of each image and places them into `/square`, `/landscape`, or `/vertical` folders.
3. Converts .png images into .jpg format.
4. Generates `images.txt` files in each of the image folders listing the image filenames.
5. Changes video names in the `/videos` folder into a hash.
6. Generates `videos.txt` file in the `/videos` folder listing the video filenames.
'''

import os
import hashlib
import shutil
from PIL import Image

def hash_file(filepath, blocksize=65536):
    hasher = hashlib.sha1()
    with open(filepath, 'rb') as afile:
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
    return hasher.hexdigest()[:10]

def process_images(directory):
    parent_dir = os.path.dirname(directory)
    square_dir = os.path.join(parent_dir, 'square')
    landscape_dir = os.path.join(parent_dir, 'landscape')
    vertical_dir = os.path.join(parent_dir, 'vertical')

    # Ensure the output directories exist
    os.makedirs(square_dir, exist_ok=True)
    os.makedirs(landscape_dir, exist_ok=True)
    os.makedirs(vertical_dir, exist_ok=True)

    # Prepare lists to hold image filenames for each category
    square_images = []
    landscape_images = []
    vertical_images = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            name, ext = os.path.splitext(filename)

            if ext.lower() in ['.png', '.jpg', '.jpeg']:
                file_hash = hash_file(filepath)
                new_filename = f"{file_hash}"

                # Open the image to get its dimensions
                with Image.open(filepath) as img:
                    width, height = img.size

                    # Determine aspect ratio category
                    if width == height:
                        aspect = 'square'
                        img_dir = square_dir
                        image_list = square_images
                    elif width > height:
                        aspect = 'landscape'
                        img_dir = landscape_dir
                        image_list = landscape_images
                    else:
                        aspect = 'vertical'
                        img_dir = vertical_dir
                        image_list = vertical_images

                    new_jpg_filename = f"{new_filename}.jpg"
                    new_jpg_path = os.path.join(img_dir, new_jpg_filename)

                    # Convert to JPG if necessary
                    if ext.lower() == '.png':
                        # Convert PNG to JPG
                        rgb_img = img.convert('RGB')
                        rgb_img.save(new_jpg_path, 'JPEG', quality=80)
                        # Rename the original PNG to hashed name (maintain in the images folder)
                        new_png_filename = f"{new_filename}.png"
                        new_png_path = os.path.join(directory, new_png_filename)
                        if filepath != new_png_path:
                            os.rename(filepath, new_png_path)
                    else:
                        # Save the JPG in the appropriate directory
                        if filepath != new_jpg_path:
                            shutil.copy2(filepath, new_jpg_path)
                        # Rename the original JPG to hashed name (maintain in the images folder)
                        new_jpg_original_path = os.path.join(directory, f"{new_filename}{ext.lower()}")
                        if filepath != new_jpg_original_path:
                            os.rename(filepath, new_jpg_original_path)

                    # Add the new jpg filename to the appropriate list
                    image_list.append(new_jpg_filename)

    # Write the images.txt files in each directory
    for dir_path, images in zip([square_dir, landscape_dir, vertical_dir],
                                [square_images, landscape_images, vertical_images]):
        images_txt_path = os.path.join(dir_path, 'images.txt')
        with open(images_txt_path, 'w') as f:
            for img_name in images:
                f.write(f"{img_name}\n")

def process_videos(directory):
    video_list = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            name, ext = os.path.splitext(filename)
            if ext.lower() == '.mp4':
                file_hash = hash_file(filepath)
                new_filename = f"{file_hash}.mp4"
                new_path = os.path.join(directory, new_filename)
                if filepath != new_path:
                    os.rename(filepath, new_path)
                video_list.append(new_filename)
    
    # Write the videos.txt file in the video directory
    videos_txt_path = os.path.join(directory, 'videos.txt')
    with open(videos_txt_path, 'w') as f:
        for video_name in video_list:
            f.write(f"{video_name}\n")

# Directory where images are stored
image_dir = os.path.join(os.getcwd(), "images")
video_dir = os.path.join(os.getcwd(), "videos")

# Process all images in the specified directory and log them
process_images(image_dir)

# Process all videos in the specified video directory
process_videos(video_dir)