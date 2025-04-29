# train_dalek.py

from ultralytics import YOLO

def main():
    model = YOLO("yolov5su.pt")  # or "yolov8n.pt" if using YOLOv8

    model.train(
        data="data.yaml",
        epochs=50,
        imgsz=640,
        batch=16,
        name="dalek_detector"
    )

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()  # Not required unless creating .exe, but harmless
    main()
