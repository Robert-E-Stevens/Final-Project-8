import os
import shutil
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler
from PIL import Image
import imagehash

# === CONFIG ===
SCRAPE_CONFIG = [
    ("sith_lightsabers", [
        "sith lightsaber", "red lightsaber", "darth vader lightsaber", "kylo ren lightsaber"
    ]),
    ("other_lightsabers", [
        "jedi lightsaber", "blue lightsaber", "green lightsaber", "anakin lightsaber"
    ])
]
IMG_SIZE = (640, 640)
MAX_IMAGES = 300

# === FUNCTIONS ===

def create_clean_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def download_images(class_name, keywords):
    print(f"\n[📥] Downloading images for: {class_name}")
    folder = class_name
    create_clean_dir(folder)

    for keyword in keywords:
        print(f"  🔍 Searching: {keyword}")
        GoogleImageCrawler(storage={'root_dir': folder}).crawl(keyword=keyword, max_num=MAX_IMAGES // 2)
        BingImageCrawler(storage={'root_dir': folder}).crawl(keyword=keyword, max_num=MAX_IMAGES // 2)

def clean_and_resize(folder):
    print(f"[🧹] Cleaning and resizing: {folder}")
    hashes = set()
    for fname in os.listdir(folder):
        fpath = os.path.join(folder, fname)
        try:
            with Image.open(fpath) as img:
                img = img.convert("RGB")
                h = imagehash.average_hash(img)
                if h in hashes:
                    os.remove(fpath)
                    continue
                hashes.add(h)
                img = img.resize(IMG_SIZE)
                img.save(fpath)
        except Exception as e:
            print(f"  ⚠️ Skipping {fname}: {e}")
            os.remove(fpath)

# === MAIN ===
def main():
    for class_name, keywords in SCRAPE_CONFIG:
        download_images(class_name, keywords)
        clean_and_resize(class_name)
    print("\n[✓] Lightsaber dataset ready!")

if __name__ == "__main__":
    main()
