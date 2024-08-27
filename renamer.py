### This script renames files in `/images`

import os
import hashlib
import shutil

def hash_file(filepath, blocksize=65536):
    hasher = hashlib.sha1()
    with open(filepath, 'rb') as afile:
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
    return hasher.hexdigest()[:10]

def rename_files(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            name, ext = os.path.splitext(filename)
            if len(name) == 10 and all(c in '0123456789abcdef' for c in name):
                continue
            
            file_hash = hash_file(filepath)
            new_filename = f"{file_hash}{ext}"
            new_filepath = os.path.join(directory, new_filename)
            
            if filepath != new_filepath:
                shutil.move(filepath, new_filepath)
                print(f'Renamed: {filename} to {new_filename}')

# Define the path to the images directory explicitly
# This can be an absolute path or relative to the current working directory
image_dir = os.path.join(os.getcwd(), "images")  # This assumes 'images' is in the same directory as the script

# Ensure the directory exists
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

# Rename all files in the specified directory
rename_files(image_dir)