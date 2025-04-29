import os
import shutil
import random

# Set random seed for reproducibility
random.seed(42)

# Corrected source folders
sith_folder = r"C:\Users\Subsi\Documents\ECEN\ECEN_5060-DeepLearning\FinalProject\FinalProject\Final-Project-8\Code\sith_lightsabers"
other_folder = r"C:\Users\Subsi\Documents\ECEN\ECEN_5060-DeepLearning\FinalProject\FinalProject\Final-Project-8\Code\other_lightsabers"

# Target dataset root
dataset_root = r"C:\Users\Subsi\Documents\ECEN\ECEN_5060-DeepLearning\FinalProject\FinalProject\Final-Project-8\Code\lightsaber_dalek_people_dataset"

# Destination folders
train_images = os.path.join(dataset_root, 'train', 'images')
train_labels = os.path.join(dataset_root, 'train', 'labels')
val_images = os.path.join(dataset_root, 'val', 'images')
val_labels = os.path.join(dataset_root, 'val', 'labels')

# Helper function to process a folder
def process_folder(source_folder, prefix):
    # Get all image-label pairs
    image_files = [f for f in os.listdir(source_folder) if f.lower().endswith('.jpg')]

    # Only keep images that have a matching .txt label
    valid_files = []
    for img_file in image_files:
        base_name = os.path.splitext(img_file)[0]
        label_file = base_name + ".txt"
        if os.path.exists(os.path.join(source_folder, label_file)):
            valid_files.append(img_file)
        else:
            print(f"⚠️ Skipping {img_file} (no label found)")

    # Shuffle
    random.shuffle(valid_files)

    # Split
    split_index = int(len(valid_files) * 0.8)
    train_files = valid_files[:split_index]
    val_files = valid_files[split_index:]

    print(f"📂 {prefix}: {len(train_files)} train, {len(val_files)} val")

    # Copy function
    def copy_files(file_list, split_images, split_labels):
        for img_file in file_list:
            base_name = os.path.splitext(img_file)[0]
            label_file = base_name + ".txt"

            # Source paths
            img_src = os.path.join(source_folder, img_file)
            label_src = os.path.join(source_folder, label_file)

            # Prefixed target paths
            new_img_name = prefix + base_name + ".jpg"
            new_label_name = prefix + base_name + ".txt"

            img_dst = os.path.join(split_images, new_img_name)
            label_dst = os.path.join(split_labels, new_label_name)

            # Copy files
            shutil.copy2(img_src, img_dst)
            shutil.copy2(label_src, label_dst)

    # Copy to train
    copy_files(train_files, train_images, train_labels)

    # Copy to val
    copy_files(val_files, val_images, val_labels)

# Process Sith
process_folder(sith_folder, prefix="sith_")

# Process Other
process_folder(other_folder, prefix="other_")

print("\n🎯 Completed fresh addition of Sith and Other lightsabers with 80/20 split!")
