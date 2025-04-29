import os
import shutil
import random
import xml.etree.ElementTree as ET

# === CONFIGURATION ===
SITH_DIR = "sith_lightsabers"
OTHER_DIR = "other_lightsabers"
MERGE_DIR = "merged_lightsabers"
DEST_ROOT = "lightsaber_dataset"
TRAIN_RATIO = 0.8  # 80% training, 20% validation

CLASS_LIST = ["sith lightsaber", "other lightsaber"]

# === STEP 1: Merge + Rename Images and XMLs ===

def create_merge_folder():
    if os.path.exists(MERGE_DIR):
        shutil.rmtree(MERGE_DIR)
    os.makedirs(MERGE_DIR)

def merge_and_rename(source_dir, prefix):
    files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.xml'))]
    for idx, file in enumerate(sorted(files)):
        base, ext = os.path.splitext(file)
        new_name = f"{prefix}_{idx:05d}{ext.lower()}"
        src_path = os.path.join(source_dir, file)
        dst_path = os.path.join(MERGE_DIR, new_name)
        shutil.copy(src_path, dst_path)

def merge_all_sources():
    print("[🔀] Merging and renaming files...")
    create_merge_folder()
    merge_and_rename(SITH_DIR, "sith")
    merge_and_rename(OTHER_DIR, "other")
    print("[✓] Merge complete.")

# === STEP 2: Convert XML to YOLO ===

def create_output_structure():
    for split in ['train', 'val']:
        os.makedirs(os.path.join(DEST_ROOT, 'images', split), exist_ok=True)
        os.makedirs(os.path.join(DEST_ROOT, 'labels', split), exist_ok=True)

def get_all_xml_files(source_dir):
    return [f for f in os.listdir(source_dir) if f.lower().endswith('.xml')]

def convert_xml_to_yolo():
    print("[📄] Converting XML to YOLO labels...")
    xml_files = get_all_xml_files(MERGE_DIR)

    if not xml_files:
        print("[⚠️] No XML files found!")
        return {}

    print(f"[👀] Found {len(xml_files)} XML files.")

    yolo_labels = {}

    for file in xml_files:
        xml_path = os.path.join(MERGE_DIR, file)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        img_w = int(root.find("size/width").text)
        img_h = int(root.find("size/height").text)

        lines = []
        for obj in root.findall("object"):
            cls = obj.find("name").text.lower().strip()
            if cls not in CLASS_LIST:
                continue
            cls_id = CLASS_LIST.index(cls)

            bbox = obj.find("bndbox")
            xmin = int(float(bbox.find("xmin").text))
            ymin = int(float(bbox.find("ymin").text))
            xmax = int(float(bbox.find("xmax").text))
            ymax = int(float(bbox.find("ymax").text))

            x_center = ((xmin + xmax) / 2) / img_w
            y_center = ((ymin + ymax) / 2) / img_h
            width = (xmax - xmin) / img_w
            height = (ymax - ymin) / img_h

            lines.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

        if lines:
            base_name = file.replace(".xml", "").replace(".XML", "")
            yolo_labels[base_name] = lines

    print(f"[✓] Converted {len(yolo_labels)} XML files.")
    return yolo_labels

# === STEP 3: Copy Images and Split into Train/Val ===

def split_and_copy(yolo_labels):
    print("[🚚] Copying images and labels into train/val folders...")

    image_files = [f for f in os.listdir(MERGE_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    image_files = [f for f in image_files if os.path.splitext(f)[0] in yolo_labels]

    random.shuffle(image_files)
    split_idx = int(len(image_files) * TRAIN_RATIO)

    train_files = image_files[:split_idx]
    val_files = image_files[split_idx:]

    for split, files in [('train', train_files), ('val', val_files)]:
        for fname in files:
            base = os.path.splitext(fname)[0]
            img_src = os.path.join(MERGE_DIR, fname)

            img_dst = os.path.join(DEST_ROOT, 'images', split, fname)
            label_dst = os.path.join(DEST_ROOT, 'labels', split, base + ".txt")

            shutil.copy(img_src, img_dst)

            with open(label_dst, "w") as f:
                f.write("\n".join(yolo_labels[base]))

    print(f"[✓] Split complete: {len(train_files)} train / {len(val_files)} val images.")

# === MAIN ===

def main():
    merge_all_sources()
    create_output_structure()
    yolo_labels = convert_xml_to_yolo()
    split_and_copy(yolo_labels)
    print("\n[🏁] Lightsaber dataset is READY!")

if __name__ == "__main__":
    main()
