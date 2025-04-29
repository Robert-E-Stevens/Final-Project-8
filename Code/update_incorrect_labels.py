import os
import shutil

# Source and Destination paths
source_base = r"C:\Users\Subsi\Documents\ECEN\ECEN_5060-DeepLearning\FinalProject\FinalProject\Final-Project-8\Code\train"
dest_base = r"C:\Users\Subsi\Documents\ECEN\ECEN_5060-DeepLearning\FinalProject\FinalProject\Final-Project-8\Code\lightsaber_dalek_people_dataset"

# Folders to process
splits = ['train', 'val']
subfolders = ['images', 'labels']

for split in splits:
    for subfolder in subfolders:
        src_folder = os.path.join(source_base, split, subfolder)
        dst_folder = os.path.join(dest_base, split, subfolder)

        if not os.path.exists(src_folder):
            print(f"Warning: {src_folder} does not exist. Skipping...")
            continue

        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)

        for filename in os.listdir(src_folder):
            src_file = os.path.join(src_folder, filename)
            dst_file = os.path.join(dst_folder, filename)

            # If a file already exists with the same name, rename it to avoid overwriting
            if os.path.exists(dst_file):
                name, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(dst_file):
                    new_filename = f"{name}_{counter}{ext}"
                    dst_file = os.path.join(dst_folder, new_filename)
                    counter += 1

            shutil.move(src_file, dst_file)
            print(f"Moved {src_file} -> {dst_file}")

print("✅ Done moving and merging sith/other lightsaber data!")
