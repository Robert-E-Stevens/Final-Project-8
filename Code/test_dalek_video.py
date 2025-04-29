from ultralytics import YOLO
import os

# === CONFIGURATION ===
MODEL_PATH = "runs/detect/dalek_detector7/weights/best.pt"  # path to trained model
INPUT_VIDEO = "daleks.mp4"                        # your input video
OUTPUT_DIR = "runs/predict"                                # YOLO will save output here
CONFIDENCE_THRESHOLD = 0.5                                 # optional: tweak if needed

# === LOAD MODEL ===
model = YOLO(MODEL_PATH)

# === RUN PREDICTION ===
results = model.predict(
    source=INPUT_VIDEO,
    conf=CONFIDENCE_THRESHOLD,
    save=True,
    save_txt=False,
    show=True  # set to False if you don’t want a popup window
)

# === RESULT INFO ===
print("\n[✓] Inference complete.")
print(f"[📁] Output video saved to: {OUTPUT_DIR}")
print(f"[🎯] Model: {MODEL_PATH}")
print(f"[🎥] Input: {INPUT_VIDEO}")
