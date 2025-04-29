import os
import shutil

# === CONFIGURATION ===
DATASETS = [
    {"prefix": "dalek", "path": "datasets/dalek_dataset_split", "class_offset": 3},  # dalek = 3
    {"prefix": "saber", "path": "lightsaber_dataset", "class_offset": 4}, # sith/other lightsaber = 4/5
]

DEST_ROOT = "lightsaber_dalek_dataset"

# === FUNCTIONS ===

def create_output_folders():
    for split in ['images/train', 'images/val', 'labels/train', 'labels/val']:
        os.makedirs(os.path.join(DEST_ROOT, split), exist_ok=True)

def adjust_and_copy(source_dir, prefix, class_offset):
    for split in ['train', 'val']:
        image_src_dir = os.path.join(source_dir, 'images', split)
        label_src_dir = os.path.join(source_dir, 'labels', split)

        images = [f for f in os.listdir(image_src_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        for idx, img_file in enumerate(sorted(images)):
            base_name, ext = os.path.splitext(img_file)
            new_base_name = f"{prefix}_{idx:05d}"
            
            img_src = os.path.join(image_src_dir, img_file)
            img_dst = os.path.join(DEST_ROOT, f'images/{split}', new_base_name + ext.lower())
            shutil.copy(img_src, img_dst)

            label_src = os.path.join(label_src_dir, base_name + ".txt")
            label_dst = os.path.join(DEST_ROOT, f'labels/{split}', new_base_name + ".txt")

            if os.path.exists(label_src):
                with open(label_src, "r") as f:
                    lines = f.readlines()

                adjusted_lines = []
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        cls = int(parts[0]) + class_offset
                        rest = parts[1:]
                        adjusted_line = f"{cls} {' '.join(rest)}"
                        adjusted_lines.append(adjusted_line)

                with open(label_dst, "w") as f:
                    f.write("\n".join(adjusted_lines))

def main():
    create_output_folders()

    for dataset in DATASETS:
        adjust_and_copy(dataset["path"], dataset["prefix"], dataset["class_offset"])

    print("\n[🏁] Dalek and Lightsaber datasets merged successfully!")

if __name__ == "__main__":
    main()
