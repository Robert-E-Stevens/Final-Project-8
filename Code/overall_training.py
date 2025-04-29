from ultralytics import YOLO

def main():
    model = YOLO('yolov8s.pt')  # or 'yolov8s.pt' if using YOLOv8
    model.train(
        data="data_5.yaml",      # 🚀 << Use the new YAML file here!
        epochs=20,
        imgsz=640,
        batch=16,
        name="combined_detector"
    )

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    main()
