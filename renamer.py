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
    # Path to the log file in the same directory as this script
    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images.txt')
    
    with open(log_file_path, 'w') as log:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                name, ext = os.path.splitext(filename)
                
                # Check if the file already has a hash name
                if len(name) == 10 and all(c in '0123456789abcdef' for c in name):
                    log.write(f"{filename}\n")
                    continue
                
                file_hash = hash_file(filepath)
                new_filename = f"{file_hash}{ext}"
                new_filepath = os.path.join(directory, new_filename)
                
                if filepath != new_filepath:
                    shutil.move(filepath, new_filepath)
                    log.write(f"{new_filename}  # Renamed from {filename}\n")
                    print(f'Renamed: {filename} to {new_filename}')
                else:
                    log.write(f"{filename}\n")

# Directory where images are stored
image_dir = os.path.join(os.getcwd(), "images")

# Ensure the directory exists
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

# Rename all files in the specified directory and log them
rename_files(image_dir)