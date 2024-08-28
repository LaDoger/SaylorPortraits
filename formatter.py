'''
This script:
1. Changes image names in the `/images` folder into a hash.
2. Converts .png images into .jpg and saves them in `/jpg`.
3. Renames any existing .png images to match the new .jpg names (except file extension).
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
    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images.txt')
    parent_dir = os.path.dirname(directory)
    jpg_dir = os.path.join(parent_dir, 'jpg')
    
    if not os.path.exists(jpg_dir):
        os.makedirs(jpg_dir)
    
    with open(log_file_path, 'w') as log:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                name, ext = os.path.splitext(filename)
                
                if ext.lower() in ['.png', '.jpg']:
                    file_hash = hash_file(filepath)
                    new_jpg_filename = f"{file_hash}.jpg"
                    
                    if ext.lower() == '.png':
                        # Convert PNG to JPG
                        new_jpg_path = os.path.join(jpg_dir, new_jpg_filename)
                        convert_png_to_jpg(filepath, jpg_dir, file_hash)

                        # Rename the original PNG to a hashed name for consistency
                        new_png_path = os.path.join(directory, f"{file_hash}{ext}")
                        if filepath != new_png_path:
                            shutil.move(filepath, new_png_path)
                    
                    elif ext.lower() == '.jpg':
                        # Rename JPG with the hashed name
                        new_jpg_path = os.path.join(jpg_dir, new_jpg_filename)
                        if filepath != new_jpg_path:
                            shutil.move(filepath, new_jpg_path)
                    
                    # Log only the new .jpg filename
                    log.write(f"{new_jpg_filename}\n")

def convert_png_to_jpg(png_path, jpg_dir, name):
    with Image.open(png_path) as img:
        rgb_img = img.convert('RGB')
        jpg_path = os.path.join(jpg_dir, f"{name}.jpg")
        rgb_img.save(jpg_path, 'JPEG', quality=80)

# Directory where images are stored
image_dir = os.path.join(os.getcwd(), "images")

# Process all images in the specified directory and log them
process_images(image_dir)