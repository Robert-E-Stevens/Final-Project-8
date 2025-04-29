from ultralytics import YOLO

def main():
    model = YOLO("yolov5su.pt")  # pretrained small model with Ultralytics
    model.train(
        data="data_2.yaml",
        epochs=50,
        imgsz=640,
        batch=16,
        name="lightsaber_detector"
    )

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    main()
