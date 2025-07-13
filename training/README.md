# Training Pipeline

This folder contains everything related to training a YOLOv5 model for basketball ball detection using the [Roboflow](https://roboflow.com/) dataset and the Ultralytics YOLO interface.

## 📂 Contents

- `player_detection.py` — Main script to download the dataset and train the YOLOv5 player detection model.
- `ball_detection.py` - Script to download the dataset and train the YOLOv5 ball detection model.
- `get_weights.py` — Script to load the trained model weights and run experiments.
- `dataset_config.py` — Utility script to fix or adjust the dataset folder structure.

## 🎯 Training Details

- **Model:** YOLOv5 (version: `yolov5l6u`)
- **Epochs:** 100 (For player detection) and 250 (For ball detection)
- **Image Size:** 640×640
- **Dataset:** Roboflow (`basketball-players-fy4c2-vfsuv`, version 17)

## 📥 Download Trained Weights

The trained model weights are available on Google Drive:

🔗 [Download `best.pt` weights from Google Drive](https://drive.google.com/your-weights-link-here)


## 🧪 Run Experiments with Pretrained Weights

To use the trained model directly without retraining, run:

```bash
python get_weights.py
```
