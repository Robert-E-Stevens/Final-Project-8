from ultralytics import YOLO
import cv2

# === CONFIGURATION ===
MODEL_PATH = "runs/detect/combined_detector2/weights/best.pt"  # ✅ your trained model
INPUT_VIDEO = "input_video_people_dog.mp4"                            # 🔥 CHANGE this to your video filename
OUTPUT_VIDEO = "output_detected_video.mp4"                      # ✅ output filename

def main():
    # Load model
    model = YOLO(MODEL_PATH)

    # Open video
    cap = cv2.VideoCapture(INPUT_VIDEO)
    if not cap.isOpened():
        print(f"❌ Error opening video {INPUT_VIDEO}")
        return

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, fps, (width, height))

    print(f"🎥 Processing {INPUT_VIDEO}...")
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run inference
        results = model.predict(frame, imgsz=640, conf=0.25)

        # Get annotated frame
        annotated_frame = results[0].plot()

        # Write frame
        out.write(annotated_frame)

        # (Optional) Show the frame live
        cv2.imshow('YOLO Detection', annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_idx += 1
        if frame_idx % 30 == 0:
            print(f"🖼️ Processed {frame_idx} frames...")

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"✅ Done! Saved annotated video to {OUTPUT_VIDEO}")

if __name__ == "__main__":
    main()
