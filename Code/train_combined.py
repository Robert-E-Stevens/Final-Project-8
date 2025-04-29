from ultralytics import YOLO

def main():
    # Load the starting model - you can use 'yolov8s.pt' or your previous best weights
    model = YOLO('yolov8s.pt')  # or 'runs/detect/combined_detector_final/weights/best.pt'

    model.train(
        data="data_6.yaml",             #  Corrected dataset config (not data_6.yaml anymore)
        epochs=50,                    #  Keep at 50 epochs
        imgsz=640,                    #  640x640 images
        batch=16,                     #  Batch size
        freeze=None,                  #  No frozen layers
        name="combined_detector_final_fresh", #  Save to a *new* project directory
        deterministic=True            #  For reproducibility
    )

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    main()
