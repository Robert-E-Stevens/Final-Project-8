import os
import random
import shutil

# Paths
SOURCE_DIR = "dalek_dataset"
DEST_DIR = "dalek_dataset_split"
TRAIN_RATIO = 0.8  # 80% train, 20% val

def create_folder_structure():
    for split in ['train', 'val']:
        os.makedirs(os.path.join(DEST_DIR, 'images', split), exist_ok=True)
        os.makedirs(os.path.join(DEST_DIR, 'labels', split), exist_ok=True)

def split_dataset():
    image_files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.jpg')]
    random.shuffle(image_files)
    split_idx = int(len(image_files) * TRAIN_RATIO)

    train_files = image_files[:split_idx]
    val_files = image_files[split_idx:]

    for split, file_list in [('train', train_files), ('val', val_files)]:
        for fname in file_list:
            base = os.path.splitext(fname)[0]
            img_src = os.path.join(SOURCE_DIR, base + ".jpg")
            label_src = os.path.join(SOURCE_DIR, base + ".txt")

            img_dst = os.path.join(DEST_DIR, 'images', split, base + ".jpg")
            label_dst = os.path.join(DEST_DIR, 'labels', split, base + ".txt")

            shutil.copy(img_src, img_dst)
            if os.path.exists(label_src):
                shutil.copy(label_src, label_dst)

    print(f"[✓] Split complete: {len(train_files)} train / {len(val_files)} val")

if __name__ == "__main__":
    create_folder_structure()
    split_dataset()
