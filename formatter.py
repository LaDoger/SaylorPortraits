import os
import hashlib
import shutil
import cv2
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

    os.makedirs(square_dir, exist_ok=True)
    os.makedirs(landscape_dir, exist_ok=True)
    os.makedirs(vertical_dir, exist_ok=True)

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

                with Image.open(filepath) as img:
                    width, height = img.size
                    if width == height:
                        aspect = 'square'
                        img_dir = square_dir
                        image_list = square_images
                        thumb_size = (512, 512)  # Square thumbnails: 512x512
                    elif width > height:
                        aspect = 'landscape'
                        img_dir = landscape_dir
                        image_list = landscape_images
                        scale = 512 / width
                        thumb_size = (512, int(height * scale))  # Longer side 512
                    else:
                        aspect = 'vertical'
                        img_dir = vertical_dir
                        image_list = vertical_images
                        scale = 512 / height
                        thumb_size = (int(width * scale), 512)  # Longer side 512

                    # Generate thumbnail
                    thumb_img = img.resize(thumb_size, Image.LANCZOS)
                    thumb_jpg_filename = f"{new_filename}_thumb.jpg"
                    thumb_jpg_path = os.path.join(img_dir, thumb_jpg_filename)
                    thumb_img.convert('RGB').save(thumb_jpg_path, 'JPEG', quality=80)

                    # Save full-size image
                    full_jpg_filename = f"{new_filename}.jpg"
                    full_jpg_path = os.path.join(img_dir, full_jpg_filename)
                    if ext.lower() == '.png':
                        img.convert('RGB').save(full_jpg_path, 'JPEG', quality=95)
                    else:
                        # Use copy2 only if the paths are different to avoid SameFileError
                        if filepath != full_jpg_path:
                            shutil.copy2(filepath, full_jpg_path)
                        else:
                            # If paths are the same, skip the copy but ensure the file exists
                            if not os.path.exists(full_jpg_path):
                                shutil.copy2(filepath, full_jpg_path)

                    # Rename original file
                    new_original_filename = f"{new_filename}{ext.lower()}"
                    new_original_path = os.path.join(directory, new_original_filename)
                    if filepath != new_original_path:
                        os.rename(filepath, new_original_path)

                    image_list.append(thumb_jpg_filename)

    # Write images.txt
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

                video = cv2.VideoCapture(filepath)
                success, frame = video.read()
                if success:
                    thumbnail_filename = f"{file_hash}.jpg"
                    thumbnail_path = os.path.join(directory, thumbnail_filename)
                    cv2.imwrite(thumbnail_path, frame)
                video.release()

                if filepath != new_path:
                    os.rename(filepath, new_path)
                video_list.append(new_filename)

    videos_txt_path = os.path.join(directory, 'videos.txt')
    with open(videos_txt_path, 'w') as f:
        for video_name in video_list:
            f.write(f"{video_name}\n")

def process_frens(directory):
    os.makedirs(directory, exist_ok=True)
    frens_list = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            name, ext = os.path.splitext(filename)
            if ext.lower() in ['.jpg', '.jpeg']:
                file_hash = hash_file(filepath)
                new_filename = f"{file_hash}"

                with Image.open(filepath) as img:
                    thumb_img = img.resize((512, 512), Image.LANCZOS)  # Treat as square
                    thumb_jpg_filename = f"{new_filename}_thumb.jpg"
                    thumb_jpg_path = os.path.join(directory, thumb_jpg_filename)
                    thumb_img.convert('RGB').save(thumb_jpg_path, 'JPEG', quality=80)

                    full_jpg_filename = f"{new_filename}.jpg"
                    full_jpg_path = os.path.join(directory, full_jpg_filename)
                    # Use copy2 only if the paths are different to avoid SameFileError
                    if filepath != full_jpg_path:
                        shutil.copy2(filepath, full_jpg_path)
                    else:
                        # If paths are the same, skip the copy but ensure the file exists
                        if not os.path.exists(full_jpg_path):
                            shutil.copy2(filepath, full_jpg_path)

                    new_original_filename = f"{new_filename}{ext.lower()}"
                    new_original_path = os.path.join(directory, new_original_filename)
                    if filepath != new_original_path:
                        os.rename(filepath, new_original_path)

                    frens_list.append(thumb_jpg_filename)

    frens_txt_path = os.path.join(directory, 'frens.txt')
    with open(frens_txt_path, 'w') as f:
        for fren_name in frens_list:
            f.write(f"{fren_name}\n")

def process_scifi(directory):
    os.makedirs(directory, exist_ok=True)
    scifi_list = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            name, ext = os.path.splitext(filename)
            if ext.lower() == '.jpg':
                file_hash = hash_file(filepath)
                new_filename = f"{file_hash}"

                with Image.open(filepath) as img:
                    thumb_img = img.resize((512, 512), Image.LANCZOS)  # Treat as square
                    thumb_jpg_filename = f"{new_filename}_thumb.jpg"
                    thumb_jpg_path = os.path.join(directory, thumb_jpg_filename)
                    thumb_img.convert('RGB').save(thumb_jpg_path, 'JPEG', quality=80)

                    full_jpg_filename = f"{new_filename}.jpg"
                    full_jpg_path = os.path.join(directory, full_jpg_filename)
                    # Use copy2 only if the paths are different to avoid SameFileError
                    if filepath != full_jpg_path:
                        shutil.copy2(filepath, full_jpg_path)
                    else:
                        # If paths are the same, skip the copy but ensure the file exists
                        if not os.path.exists(full_jpg_path):
                            shutil.copy2(filepath, full_jpg_path)

                    new_original_filename = f"{new_filename}{ext.lower()}"
                    new_original_path = os.path.join(directory, new_original_filename)
                    if filepath != new_original_path:
                        os.rename(filepath, new_original_path)

                    scifi_list.append(thumb_jpg_filename)

    scifi_txt_path = os.path.join(directory, 'scifi.txt')
    with open(scifi_txt_path, 'w') as f:
        for scifi_name in scifi_list:
            f.write(f"{scifi_name}\n")

# Directory paths
image_dir = os.path.join(os.getcwd(), "images")
video_dir = os.path.join(os.getcwd(), "videos")
frens_dir = os.path.join(os.getcwd(), "frens")
scifi_dir = os.path.join(os.getcwd(), "scifi")

# Process everything
process_images(image_dir)
process_videos(video_dir)
process_frens(frens_dir)
process_scifi(scifi_dir)