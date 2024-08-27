'''
This script:
1. Changes image names in the `/images` folder into a hash.
2. Convert those .png images into .jpg and save in `/jpg`
3. Saves a list of all images in `images.txt` for the browser to fetch.
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
                
                # Skip if already processed or not a PNG we're interested in
                if len(name) == 10 and all(c in '0123456789abcdef' for c in name) or ext.lower() != '.png':
                    if ext.lower() == '.png':
                        # Check if JPG counterpart exists
                        if not os.path.exists(os.path.join(jpg_dir, f"{name}.jpg")):
                            convert_png_to_jpg(filepath, jpg_dir, name)
                        log.write(f"{name}.jpg\n")
                    else:
                        log.write(f"{filename}\n")
                    continue
                
                file_hash = hash_file(filepath)
                new_name = f"{file_hash}"
                
                if ext.lower() == '.png':
                    jpg_path = os.path.join(jpg_dir, f"{new_name}.jpg")
                    if not os.path.exists(jpg_path):
                        convert_png_to_jpg(filepath, jpg_dir, new_name)
                    log.write(f"{new_name}.jpg  # Converted from {filename}\n")
                    print(f'Converted: {filename} to {new_name}.jpg')
                else:
                    # For non-PNG files, just rename
                    new_filename = f"{new_name}{ext}"
                    new_filepath = os.path.join(directory, new_filename)
                    if filepath != new_filepath:
                        shutil.move(filepath, new_filepath)
                        log.write(f"{new_filename}  # Renamed from {filename}\n")
                        print(f'Renamed: {filename} to {new_name}{ext}')
                    else:
                        log.write(f"{filename}\n")

def convert_png_to_jpg(png_path, jpg_dir, name):
    with Image.open(png_path) as img:
        rgb_img = img.convert('RGB')
        jpg_path = os.path.join(jpg_dir, f"{name}.jpg")
        rgb_img.save(jpg_path, 'JPEG', quality=80)

# Directory where images are stored
image_dir = os.path.join(os.getcwd(), "images")

# Process all images in the specified directory and log them
process_images(image_dir)