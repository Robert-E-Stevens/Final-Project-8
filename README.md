# Deep Learning Object Detection Project

## Overview
This project uses a deep learning object detection model to detect and classify:
- People
- Cats
- Dogs
- Daleks
- Sith Lightsabers
- Other Lightsabers

The model is based on [Ultralytics YOLOv8](https://docs.ultralytics.com/) and was trained on a custom dataset combined with COCO subset classes.

---

## Installation

Clone the repository:
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
python -m pip install --upgrade pip

Install Python dependencies:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install ultralytics
pip install -r requirements.txt  # if available

Usage
Run Inference Video
python predict_combined.py --source combined_videos.mp4 --weights runs/detect/combined_detector_final_fresh4/weights/best.pt

Run Training (optional)
python train_combined.py

Repository Structure:
| Folder/File | Description |
|-------------|-------------|
| `train_combined.py` | Training script |
| `predict_combined.py` | Inference script |
| `requirements.txt` | Dependency list |
| `data.yaml` | Dataset configuration |
| `runs/detect/` | Model training outputs |
| `.github/workflows/` | GitHub Actions CI/CD workflows |

Pydoc Documentation
Full Python documentation generated with pydoc is available here (hosted on GitHub if published to GitHub Pages).

License
This project is for academic coursework and personal experimentation only.

Acknowledgements
Ultralytics YOLOv8

Microsoft COCO Dataset

Custom Scraped Datasets
