import os
import json
import shutil
import cv2

# === CONFIGURATION ===
ANNOTATIONS_PATH = "annotations/instances_val2017.json"  # Path to your annotations file
IMAGES_DIR = "val2017"  # Folder containing COCO images
OUTPUT_DIR = "coco_subset_yolo"  # Output folder for filtered images and labels

# Category IDs in COCO dataset
COCO_CATEGORIES = {
    1: 0,  # person -> class 0
    17: 1, # cat -> class 1
    18: 2  # dog -> class 2
}

# === CREATE OUTPUT STRUCTURE ===
os.makedirs(os.path.join(OUTPUT_DIR, "images", "train"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "labels", "train"), exist_ok=True)

# === LOAD COCO ANNOTATIONS ===
print("[📄] Loading annotations...")
with open(ANNOTATIONS_PATH, "r") as f:
    coco = json.load(f)

# Map image IDs to file names
image_id_to_filename = {img["id"]: img["file_name"] for img in coco["images"]}

# Group annotations by image ID
image_annotations = {}
for ann in coco["annotations"]:
    if ann["category_id"] not in COCO_CATEGORIES:
        continue  # Skip unwanted classes

    image_id = ann["image_id"]
    bbox = ann["bbox"]  # (x_min, y_min, width, height)

    if image_id not in image_annotations:
        image_annotations[image_id] = []

    image_annotations[image_id].append({
        "bbox": bbox,
        "category_id": COCO_CATEGORIES[ann["category_id"]]
    })

# === CONVERT AND SAVE ===
print("[🚀] Converting annotations and copying images...")

for image_id, annotations in image_annotations.items():
    filename = image_id_to_filename[image_id]
    src_img_path = os.path.join(IMAGES_DIR, filename)
    dst_img_path = os.path.join(OUTPUT_DIR, "images", "train", filename)

    # Copy image
    shutil.copy(src_img_path, dst_img_path)

    # Create YOLO label file
    label_path = os.path.join(OUTPUT_DIR, "labels", "train", filename.replace(".jpg", ".txt"))

    with open(label_path, "w") as f:
        for ann in annotations:
            x_min, y_min, width, height = ann["bbox"]
            x_center = x_min + width / 2
            y_center = y_min + height / 2

            # Normalize coordinates
            img_width = 640  # COCO images are not fixed size, so we'll read size properly
            img_height = 480
            if os.path.exists(dst_img_path):
                img = cv2.imread(dst_img_path)
                if img is not None:
                    img_height, img_width = img.shape[:2]

            x_center /= img_width
            y_center /= img_height
            width /= img_width
            height /= img_height

            # Write line: class_id x_center y_center width height
            f.write(f"{ann['category_id']} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

print("\n✅ Done! COCO subset for Person, Cat, Dog is ready in 'coco_subset_yolo/'.")

