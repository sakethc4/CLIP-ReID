# Here is the temp script to run data labeling when we do it in collab. 
# DELETE LATER. EACH IS SUPPOSED TO REPRESENT A CELL. 
import os
import re
import glob
import shutil

# Directory where your existing labeled dataset is stored
existing_data_dir = '/content/CLIP-ReID/Market-1501-v15.09.15'

# Directories within the existing dataset
train_dir = os.path.join(existing_data_dir, 'bounding_box_train')
query_dir = os.path.join(existing_data_dir, 'query')
gallery_dir = os.path.join(existing_data_dir, 'bounding_box_test')

# Directory where your new images are stored
new_data_dir = '/content/new_images'

# Pattern to extract pid and camid from filenames
pattern = re.compile(r'([-]?\d+)_c(\d)s\d+_\d+_\d+\.jpg')

# Function to process directory
def process_new_images(dir_path, output_dir):
    img_paths = glob.glob(os.path.join(dir_path, '*.jpg'))
    dataset = []

    for img_path in sorted(img_paths):
        match = pattern.search(os.path.basename(img_path))
        if match:
            pid, camid = map(int, match.groups())
            if pid == -1 or camid == -1:
                continue  # Skip images with pid or camid as -1
            assert 1 <= camid <= 6
            camid -= 1  # index starts from 0

            # Append data in the required format
            dataset.append((img_path, pid, camid, 0))

            # Move the image to the appropriate directory
            shutil.copy(img_path, output_dir)

    return dataset

# Ensure output directories exist
os.makedirs(train_dir, exist_ok=True)
os.makedirs(query_dir, exist_ok=True)
os.makedirs(gallery_dir, exist_ok=True)

# Process new images and integrate them into the existing dataset
new_train_images = process_new_images(new_data_dir, train_dir)
new_query_images = process_new_images(new_data_dir, query_dir)
new_gallery_images = process_new_images(new_data_dir, gallery_dir)

print("New images have been labeled and integrated into the existing dataset.")