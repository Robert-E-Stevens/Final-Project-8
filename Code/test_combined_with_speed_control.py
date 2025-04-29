import cv2
import numpy as np
from ultralytics import YOLO

# Load the model
model = YOLO("runs/detect/combined_detector_final_fresh4/weights/best.pt")

# Open the video
cap = cv2.VideoCapture("combined_videos.mp4")
cv2.namedWindow("YOLOv8 Filtered Inference", cv2.WINDOW_NORMAL)

# Playback settings
delay = 50
paused = False
skip_amount = 30

print("Controls:")
print("  [+] = Speed up playback")
print("  [-] = Slow down playback")
print("  [←] = Rewind 30 frames")
print("  [→] = Skip ahead 30 frames")
print("  [space] = Pause/Unpause")
print("  [q] = Quit")



while cap.isOpened():
    if not paused:
        ret, frame = cap.read()
        if not ret:
            break

        # Run inference
        results = model(frame, imgsz=640, conf=0.3, iou=0.3, vid_stride=3)
        boxes = results[0].boxes
        class_ids = boxes.cls.cpu().numpy().astype(int)
        confidences = boxes.conf.cpu().numpy()
        xyxy = boxes.xyxy.cpu().numpy()

        indices_to_draw = []

        # Rule 1: Show only sith_lightsaber if both are present
        if 5 in class_ids and 4 in class_ids:
            indices_to_draw = [i for i, cls in enumerate(class_ids) if cls == 5]

        # Rule 2: Suppress person if cat or dog is also present
        elif 0 in class_ids and (1 in class_ids or 2 in class_ids):
            indices_to_draw = [i for i, cls in enumerate(class_ids) if cls != 0]

        # Otherwise show all
        else:
            indices_to_draw = range(len(class_ids))

        # Draw filtered boxes
        annotated_frame = frame.copy()
        for i in indices_to_draw:
            cls = class_ids[i]
            conf = confidences[i]
            x1, y1, x2, y2 = map(int, xyxy[i])
            label = f"{model.names[cls]} {conf:.2f}"

            # Optional: color-code specific classes
            if cls == 5:
                color = (0, 0, 255)  # Red for sith
            elif cls == 4:
                color = (255, 255, 0)  # Cyan for other lightsaber
            elif cls == 0:
                color = (0, 255, 255)  # Yellow for person
            else:
                color = (0, 255, 0)    # Green for others

            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(annotated_frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Resize to fit screen if necessary
        frame_h, frame_w = annotated_frame.shape[:2]
        max_w, max_h = 1280, 720  # or adjust to your screen

        if frame_w > max_w or frame_h > max_h:
            scale = min(max_w / frame_w, max_h / frame_h)
            new_size = (int(frame_w * scale), int(frame_h * scale))
            annotated_frame = cv2.resize(annotated_frame, new_size)

        cv2.imshow("YOLOv8 Filtered Inference", annotated_frame)


    # Keyboard controls
    key = cv2.waitKey(delay if not paused else 0) & 0xFF

    if key == ord('q'):
        break
    elif key in [ord('+'), ord('=')]:
        delay = max(1, delay - 10)
        print(f"Increased speed: {1000 / delay:.1f} FPS")
    elif key in [ord('-'), ord('_')]:
        delay += 10
        print(f"Decreased speed: {1000 / delay:.1f} FPS")
    elif key == ord(' '):
        paused = not paused
        print("Paused" if paused else "Resumed")
    elif key == 81 or key == 2424832:  # Left arrow
        current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, current_frame - skip_amount))
        print(f"Rewind to frame {max(0, current_frame - skip_amount)}")
        paused = True
    elif key == 83 or key == 2555904:  # Right arrow
        current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.set(cv2.CAP_PROP_POS_FRAMES, min(total_frames - 1, current_frame + skip_amount))
        print(f"Skip ahead to frame {min(total_frames - 1, current_frame + skip_amount)}")
        paused = True

# Release resources
cap.release()
cv2.destroyAllWindows()
