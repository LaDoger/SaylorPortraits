import os
import hashlib
from PIL import Image
from pathlib import Path

IMAGES_DIR = 'images'
OUTPUT_FILE = 'images.txt'

def get_file_hash(file_path):
    """Calculate MD5 hash of a file."""
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()[:8]

def process_images():
    processed_images = []
    
    if not os.path.exists(IMAGES_DIR):
        print(f"Directory {IMAGES_DIR} not found.")
        return

    # Get list of files
    files = [f for f in os.listdir(IMAGES_DIR) if os.path.isfile(os.path.join(IMAGES_DIR, f))]
    
    for filename in files:
        file_path = os.path.join(IMAGES_DIR, filename)
        
        # Skip non-image files (basic check)
        if filename.lower().endswith('.txt') or filename.startswith('.'):
            continue
            
        try:
            # Calculate hash for new filename
            file_hash = get_file_hash(file_path)
            new_filename = f"{file_hash}.jpg"
            new_file_path = os.path.join(IMAGES_DIR, new_filename)
            
            # Open image
            with Image.open(file_path) as img:
                # Convert to RGB if necessary (e.g. PNG with alpha)
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Save as optimized JPG with 80% quality, maintaining original resolution
                # Only save if it's a different file or we want to re-compress
                # For simplicity, we'll save to a temp file then rename/replace
                
                temp_path = new_file_path + ".temp"
                img.save(temp_path, 'JPEG', quality=80, optimize=True)
                
                # If the new filename is different from the old one, remove the old one
                if file_path != new_file_path:
                    os.remove(file_path)
                    os.rename(temp_path, new_file_path)
                else:
                    # If filename is same (already hashed), replace with optimized version
                    os.replace(temp_path, new_file_path)
                    
            processed_images.append(new_filename)
            print(f"Processed: {filename} -> {new_filename}")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    # Write to text file
    with open(OUTPUT_FILE, 'w') as f:
        for img_name in sorted(processed_images):
            f.write(f"{img_name}\n")
            
    print(f"Finished! List written to {OUTPUT_FILE}")

if __name__ == "__main__":
    process_images()

