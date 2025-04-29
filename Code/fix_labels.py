import os

# Path to your dataset labels
LABELS_DIR = "datasets/lightsaber_dalek_people_dataset/labels"

# Mapping of old (bad) class numbers to correct ones
# Example: class 6 -> dalek (4), class 7 or 8 -> lightsaber (3)
FIX_MAP = {
    6: 4,   # Dalek
    7: 3,   # Lightsaber
    8: 3,   # Lightsaber
}

def fix_label_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    fixed_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) > 0:
            cls = int(parts[0])
            if cls in FIX_MAP:
                parts[0] = str(FIX_MAP[cls])
            fixed_lines.append(' '.join(parts))

    with open(file_path, 'w') as f:
        f.write('\n'.join(fixed_lines))

def fix_all_labels():
    for split in ['train', 'val']:
        split_dir = os.path.join(LABELS_DIR, split)
        if not os.path.exists(split_dir):
            continue
        for filename in os.listdir(split_dir):
            if filename.endswith('.txt'):
                fix_label_file(os.path.join(split_dir, filename))

if __name__ == "__main__":
    fix_all_labels()
    print("✅ All labels fixed!")
