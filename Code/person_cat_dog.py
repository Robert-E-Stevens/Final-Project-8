from ultralytics import YOLO
import cv2

# Load your trained model
model = YOLO("runs/detect/combined_detector_final2/weights/best.pt")

# Open the video
video_path = "daleks.mp4"  # <--- UPDATE this to your video file
cap = cv2.VideoCapture(video_path)

# Video Writer (optional: to save output)
save_output = True
if save_output:
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output_video.mp4', fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run inference on the frame
    results = model.predict(frame, imgsz=640, conf=0.5)  # conf threshold 0.5

    # Draw the results on the frame
    annotated_frame = results[0].plot()

    # Display
    cv2.imshow('YOLOv8 Detection', annotated_frame)

    # Save output
    if save_output:
        out.write(annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
if save_output:
    out.release()
cv2.destroyAllWindows()
