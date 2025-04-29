from ultralytics import YOLO

# === CONFIGURATION ===
MODEL_PATH = "runs/detect/lightsaber_detector3/weights/best.pt"  # path to trained model
INPUT_VIDEO = "sith_fight.mp4"                             # your test video (adjust this!)
OUTPUT_DIR = "runs/predict"                                      # will save output here
CONFIDENCE_THRESHOLD = 0.5                                       # detection threshold

# === LOAD MODEL ===
model = YOLO(MODEL_PATH)

# === RUN INFERENCE ===
results = model.predict(
    source=INPUT_VIDEO,
    conf=CONFIDENCE_THRESHOLD,
    save=True,
    save_txt=False,
    show=True  # set to False if you don't want popup window
)

# === OUTPUT INFO ===
print("\n[✓] Inference complete!")
print(f"[📁] Output video saved to: {OUTPUT_DIR}")
print(f"[🎯] Model used: {MODEL_PATH}")
print(f"[🎥] Tested on: {INPUT_VIDEO}")
