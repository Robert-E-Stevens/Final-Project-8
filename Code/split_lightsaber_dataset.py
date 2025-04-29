import os
import random
import shutil

# === CONFIGURATION ===
SITH_IMAGES_DIR = "sith_lightsabers/images"
SITH_LABELS_DIR = "sith_lightsabers/labels"
OTHER_IMAGES_DIR = "other_lightsabers/images"
OTHER_LABELS_DIR = "other_lightsabers/labels"

DEST_ROOT = "lightsaber_dataset"
TRAIN_RATIO = 0.8  # 80% training, 20% validation

# === FUNCTIONS ===

def create_folder_structure():
    for split in ['train', 'val']:
        os.makedirs(os.path.join(DEST_ROOT, 'images', split), exist_ok=True)
        os.makedirs(os.path.join(DEST_ROOT, 'labels', split), exist_ok=True)

def gather_files(source_images_dir, source_labels_dir):
    file_list = []
    for fname in os.listdir(source_images_dir):
        if fname.endswith('.jpg'):
            base = os.path.splitext(fname)[0]
            img_path = os.path.join(source_images_dir, base + ".jpg")
            label_path = os.path.join(source_labels_dir, base + ".txt")
            if os.path.exists(img_path) and os.path.exists(label_path):
                file_list.append((img_path, label_path))
    return file_list

def split_and_copy(file_list):
    random.shuffle(file_list)
    split_idx = int(len(file_list) * TRAIN_RATIO)
    
    train_files = file_list[:split_idx]
    val_files = file_list[split_idx:]

    for split, files in [('train', train_files), ('val', val_files)]:
        for img_src, label_src in files:
            base = os.path.splitext(os.path.basename(img_src))[0]

            img_dst = os.path.join(DEST_ROOT, 'images', split, base + ".jpg")
            label_dst = os.path.join(DEST_ROOT, 'labels', split, base + ".txt")

            shutil.copy(img_src, img_dst)
            shutil.copy(label_src, label_dst)

    return len(train_files), len(val_files)

def main():
    create_folder_structure()

    print("[📥] Gathering Sith lightsaber files...")
    sith_files = gather_files(SITH_IMAGES_DIR, SITH_LABELS_DIR)

    print("[📥] Gathering Other lightsaber files...")
    other_files = gather_files(OTHER_IMAGES_DIR, OTHER_LABELS_DIR)

    total_train = total_val = 0

    print("[🔀] Splitting Sith lightsaber dataset...")
    train_sith, val_sith = split_and_copy(sith_files)
    total_train += train_sith
    total_val += val_sith

    print("[🔀] Splitting Other lightsaber dataset...")
    train_other, val_other = split_and_copy(other_files)
    total_train += train_other
    total_val += val_other

    print(f"\n[✓] Split complete: {total_train} train / {total_val} val total images")

if __name__ == "__main__":
    main()
