# main.py
import cv2
import torch
from ultralytics import YOLO
import os

# Load YOLOv5 pretrained model (COCO dataset)
model = YOLO("yolov5s.pt")  # or use yolov8n.pt

# Define COCO class IDs of interest
TARGET_CLASSES = {0: 'person', 15: 'cat', 16: 'dog'}

# Input and Output video
input_path = "input_video.mp4"
output_path = "output_annotated.mp4"

# Open video
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    raise IOError(f"Cannot open video file: {input_path}")

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

print("Processing video...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Inference
    results = model(frame, verbose=False)[0]

    # Draw detections
    for box in results.boxes:
        cls_id = int(box.cls.item())
        if cls_id in TARGET_CLASSES:
            label = TARGET_CLASSES[cls_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf.item()
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    out.write(frame)

cap.release()
out.release()
cv2.destroyAllWindows()
print(f"Done. Output saved to: {output_path}")
