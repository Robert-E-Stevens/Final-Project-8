from ultralytics import YOLO
import cv2
import numpy as np

# Define class colors
CLASS_COLORS = {
    0: (0, 0, 255),    # Blue - person
    1: (255, 0, 255),    # Magenta - dog
    2: (0, 255, 255),    # Aqua - cat
    3: (255, 255, 0),  # Cyan - dalek
    4: (0, 255, 0),  # Green - other lightsaber
    5: (255, 0, 0),  # Red - sith lightsaber
}

# Define class names
CLASS_NAMES = {
    0: "person",
    1: "dog",
    2: "cat",
    3: "dalek",
    4: "other lightsaber",
    5: "sith lightsaber",
}

def main():
    model = YOLO('runs/detect/combined_detector_final_fresh/weights/best.pt')

    # Open the video file
    video_path = 'combined_videos.mp4'
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30  # Default to 30 if FPS not readable

    # Output writer
    out = cv2.VideoWriter('sith_fight_color.mp4',
                          cv2.VideoWriter_fourcc(*'mp4v'),
                          fps,
                          (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run prediction on frame
        results = model.predict(frame, save=False, conf=0.25, verbose=False)

        # Annotate detections
        for r in results:
            if r.boxes is not None:
                for box in r.boxes:
                    cls_id = int(box.cls[0].cpu().numpy())
                    conf = float(box.conf[0].cpu().numpy())
                    xyxy = box.xyxy[0].cpu().numpy()

                    x1, y1, x2, y2 = map(int, xyxy)
                    color = CLASS_COLORS.get(cls_id, (255, 255, 255))

                    # Draw bounding box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                    # Draw label and confidence
                    label = f"{CLASS_NAMES.get(cls_id, str(cls_id))} {conf:.2f}"
                    (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                    cv2.rectangle(frame, (x1, y1 - text_height - baseline), (x1 + text_width, y1), color, -1)
                    cv2.putText(frame, label, (x1, y1 - baseline),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        # Write the frame
        out.write(frame)

        # Live preview
        cv2.imshow('YOLO Detection Preview', frame)
        if cv2.waitKey(1) == 27:  # ESC key
            print("ESC pressed. Exiting...")
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Processing complete. Video saved as 'sith_fight_color.mp4'.")

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    main()
