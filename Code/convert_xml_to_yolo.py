import os
import xml.etree.ElementTree as ET

# 🔧 CONFIGURATION
ANNOTATIONS_DIR = "dalek_dataset"        # Folder with .xml files
IMAGES_DIR = "dalek_dataset"             # Same folder with .jpg images
OUTPUT_LABELS_DIR = "dalek_dataset"      # YOLO labels saved here
CLASS_LIST = ["dalek"]                   # Only one class

def convert():
    os.makedirs(OUTPUT_LABELS_DIR, exist_ok=True)
    files = [f for f in os.listdir(ANNOTATIONS_DIR) if f.endswith(".xml")]
    count = 0

    for file in files:
        xml_path = os.path.join(ANNOTATIONS_DIR, file)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        img_w = int(root.find("size/width").text)
        img_h = int(root.find("size/height").text)

        yolo_lines = []

        for obj in root.findall("object"):
            cls = obj.find("name").text.lower().strip()
            if cls not in CLASS_LIST:
                continue
            cls_id = CLASS_LIST.index(cls)

            bbox = obj.find("bndbox")
            xmin = int(bbox.find("xmin").text)
            ymin = int(bbox.find("ymin").text)
            xmax = int(bbox.find("xmax").text)
            ymax = int(bbox.find("ymax").text)

            x_center = (xmin + xmax) / 2 / img_w
            y_center = (ymin + ymax) / 2 / img_h
            width = (xmax - xmin) / img_w
            height = (ymax - ymin) / img_h

            yolo_lines.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

        if yolo_lines:
            txt_filename = file.replace(".xml", ".txt")
            txt_path = os.path.join(OUTPUT_LABELS_DIR, txt_filename)
            with open(txt_path, "w") as f:
                f.write("\n".join(yolo_lines))
            count += 1

    print(f"[✓] Converted {count} files to YOLO format.")

if __name__ == "__main__":
    convert()
