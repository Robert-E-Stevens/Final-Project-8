import os
import shutil
import random

# === CONFIGURATION ===
COCO_DIR = "coco_subset_yolo"               # Your filtered COCO (person/cat/dog)
DALEK_LIGHTSABER_DIR = "datasets/lightsaber_dalek_dataset"  # Your dalek/lightsaber dataset
DEST_DIR = "lightsaber_dalek_people_dataset"       # New merged output
TRAIN_RATIO = 0.8  # 80% train, 20% val

# === CREATE DESTINATION STRUCTURE ===
for split in ['images/train', 'images/val', 'labels/train', 'labels/val']:
    os.makedirs(os.path.join(DEST_DIR, split), exist_ok=True)

# === COLLECT ALL FILES ===
coco_images = [f for f in os.listdir(os.path.join(COCO_DIR, 'images', 'train')) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
dalek_images = [f for f in os.listdir(os.path.join(DALEK_LIGHTSABER_DIR, 'images', 'train')) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

all_images = []

# Pack images and source info
for img in coco_images:
    all_images.append((img, COCO_DIR))
for img in dalek_images:
    all_images.append((img, DALEK_LIGHTSABER_DIR))

random.shuffle(all_images)

split_idx = int(len(all_images) * TRAIN_RATIO)
train_images = all_images[:split_idx]
val_images = all_images[split_idx:]

# === COPY FUNCTION ===
def copy_and_fix(src_img_path, src_label_path, dst_img_path, dst_label_path, source):
    if not os.path.exists(src_label_path):
        print(f"[⚠️] Missing label for {src_img_path}. Skipping.")
        return  # Skip this image

    shutil.copy(src_img_path, dst_img_path)

    # Fix labels if needed
    with open(src_label_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 5:
            continue  # skip bad lines
        cls_id, x_center, y_center, width, height = parts

        cls_id = int(cls_id)

        if source == "COCO":
            pass  # COCO labels already correct
        elif source == "DALEK":
            cls_id += 3  # Shift dalek/lightsaber classes

        new_line = f"{cls_id} {x_center} {y_center} {width} {height}\n"
        new_lines.append(new_line)

    with open(dst_label_path, 'w') as f:
        f.writelines(new_lines)

# === COPY TRAIN SET ===
for img_file, source_dir in train_images:
    img_src = os.path.join(source_dir, 'images', 'train', img_file)
    label_src = os.path.join(source_dir, 'labels', 'train', img_file.replace('.jpg', '.txt'))

    img_dst = os.path.join(DEST_DIR, 'images', 'train', img_file)
    label_dst = os.path.join(DEST_DIR, 'labels', 'train', img_file.replace('.jpg', '.txt'))

    copy_and_fix(img_src, label_src, img_dst, label_dst, "COCO" if source_dir == COCO_DIR else "DALEK")

# === COPY VAL SET ===
for img_file, source_dir in val_images:
    img_src = os.path.join(source_dir, 'images', 'train', img_file)
    label_src = os.path.join(source_dir, 'labels', 'train', img_file.replace('.jpg', '.txt'))

    img_dst = os.path.join(DEST_DIR, 'images', 'val', img_file)
    label_dst = os.path.join(DEST_DIR, 'labels', 'val', img_file.replace('.jpg', '.txt'))

    copy_and_fix(img_src, label_src, img_dst, label_dst, "COCO" if source_dir == COCO_DIR else "DALEK")

print(f"\n✅ Merge complete: {len(train_images)} train images, {len(val_images)} val images into '{DEST_DIR}'.")

