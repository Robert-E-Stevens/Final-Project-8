# Test Plan – Deep Learning Object Detection

**Project:** YOLOv8 Object Detection for People, Animals, Daleks, and Lightsabers  
**Author:** Robert Stevens  
**Date:** April 30, 2025

---

## 1. Overview

This test plan outlines unit and integration tests used to verify the functionality of the training and inference code for the object detection model. Tests are designed to ensure the system runs correctly in both development and deployment environments.

---

## 2. Unit Tests

### ✅ YOLOv8 Model Loading
- **Objective:** Ensure the YOLOv8 model loads from the correct path
- **Input:** Path to model weights (`.pt` file)
- **Expected Result:** Model initializes without error

### ✅ Data Path Validation
- **Objective:** Confirm that image and label directories exist and are formatted properly
- **Input:** `data_6.yaml` with dataset paths
- **Expected Result:** Training/inference starts without path errors

### ✅ Frame Navigation Logic
- **Objective:** Confirm pause/resume, skip, and speed control work correctly
- **Input:** User keypress events
- **Expected Result:** Playback behavior changes as expected

---

## 3. Integration Tests

### ✅ Training Pipeline Dry Run (CI)
- **Script:** `.github/workflows/ci.yml`
- **Steps Tested:** Dependency install → load model → run `train_combined.py` (without crashing)
- **Trigger:** Push to GitHub

### ✅ Inference Dry Run
- **Script:** `test_combined_with_speed_control.py`
- **Input:** `combined_videos2.mp4`, model weights
- **Expected Result:** Boxes appear on screen with correct labels and filters applied

---

## 4. Manual Tests

| Feature                | Test Description                           | Pass? |
|------------------------|--------------------------------------------|-------|
| Detect Daleks          | Load test video and confirm red boxes appear | ✅    |
| Suppress person if dog/cat | Check filtered inference in action     | ✅    |
| Lightsaber rule logic  | Confirm only Sith shown when both detected | ✅    |

---

## 5. Known Issues

- Bounding boxes for cats and dogs sometimes overlap with person due to training imbalance.
- Dataset paths must be adjusted depending on whether running locally or in CI.

---

## 6. Future Testing Enhancements

- Add automatic mAP test script (assert ≥75% for key classes)
- Add unit test for YAML parsing and video capture
- Add post-inference image saving tests
