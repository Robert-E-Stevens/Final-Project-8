import os
import shutil
from PIL import Image
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler
import imagehash

# ----------------------------- CONFIG -------------------------------- #
SAVE_DIR = "dalek_dataset"
IMG_SIZE = (640, 640)
MAX_IMAGES = 300  # per source
KEYWORDS = ["dalek doctor who", "dalek toy", "dalek scene"]
# --------------------------------------------------------------------- #

def create_clean_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def download_images():
    print("[+] Downloading images...")
    create_clean_dir(SAVE_DIR)

    for keyword in KEYWORDS:
        print(f"    > Searching: {keyword}")

        google = GoogleImageCrawler(storage={'root_dir': SAVE_DIR})
        google.crawl(keyword=keyword, max_num=MAX_IMAGES // 2)

        bing = BingImageCrawler(storage={'root_dir': SAVE_DIR})
        bing.crawl(keyword=keyword, max_num=MAX_IMAGES // 2)

def clean_images():
    print("[+] Cleaning images...")

    hashes = set()
    removed = 0
    total = 0

    for fname in os.listdir(SAVE_DIR):
        path = os.path.join(SAVE_DIR, fname)
        try:
            with Image.open(path) as img:
                img = img.convert('RGB')
                h = imagehash.average_hash(img)

                if h in hashes:
                    os.remove(path)
                    removed += 1
                else:
                    hashes.add(h)
                    total += 1

        except Exception as e:
            print(f"    Skipping {fname}: {e}")
            os.remove(path)
            removed += 1

    print(f"    > Removed {removed} images, kept {total} unique.")

def resize_images():
    print("[+] Resizing images to 640x640...")
    for fname in os.listdir(SAVE_DIR):
        path = os.path.join(SAVE_DIR, fname)
        try:
            with Image.open(path) as img:
                img = img.resize(IMG_SIZE)
                img.save(path)
        except Exception as e:
            print(f"    Failed resizing {fname}: {e}")
            os.remove(path)

def print_summary():
    files = os.listdir(SAVE_DIR)
    print(f"[✓] Dataset ready! Total usable images: {len(files)}")
    print(f"    Saved in: {os.path.abspath(SAVE_DIR)}")

if __name__ == "__main__":
    download_images()
    clean_images()
    resize_images()
    print_summary()
