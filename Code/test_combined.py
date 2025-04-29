from ultralytics import YOLO

# Load trained model
model = YOLO("runs/detect/combined_detector_final_fresh3/weights/best.pt")

# Path to your input video
input_video_path = "combined_videos.mp4"  
#output_video_path = "test_.mp4"  

# Run prediction on video
model.predict(
    source=input_video_path, 
    save=True, 
    save_txt=False, 
    save_conf=True, 
    project="runs/detect", 
    name="video_inference",
    conf=0.3,         # confidence threshold
    iou=0.3,           # IoU threshold for NMS
    imgsz=640,         # input size
    show=True,         # show live
    vid_stride=1       # predict every frame
)
