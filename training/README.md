# 🏀 Training Pipeline for Basketball Player and Ball Detection

This folder contains all the scripts required to train and test YOLOv5/YOLOv8 models on basketball video data using Roboflow datasets.

---

## 📂 Folder Contents

| File | Description |
|------|-------------|
| `player_detection.py` | Downloads dataset & trains YOLOv5 on player detection. |
| `ball_detection.py` | Downloads dataset & trains YOLOv5 on ball detection. |
| `keypoint_court.py` | Trains YOLOv8-pose model on court keypoint detection. |
| `get_weights.py` | Loads trained weights and runs inference experiments. |
| `dataset_config.py` | Utility to restructure dataset folders (if needed). |

---

## 🎯 Training Details

- **Models Used:**  
  - Player & Ball Detection: `yolov5l6u`  
  - Court Keypoint Detection: `yolov8x-pose.pt`

- **Epochs:**  
  - Player Detection: 100  
  - Ball Detection: 250  
  - Keypoints (Court): 500

- **Image Size:** 640×640

- **Datasets:**  
  - Player/Ball: [Roboflow project `basketball-players-fy4c2-vfsuv`](https://universe.roboflow.com/workspace-5ujvu/basketball-players-fy4c2-vfsuv)   
  - Court Keypoints: [Roboflow project `reloc2-den7l`](https://universe.roboflow.com/fyp-3bwmg/reloc2-den7l/dataset/1)

---

## 📥 Download Trained Weights

To use the trained model weights:

- Download from Google Drive: [`best.pt`](https://drive.google.com/file/d/1eAHfkK7xEC6IV7AkII90PFNUF82m7oot/view?usp=sharing)

- Or run inference directly:

```bash
python get_weights.py --model player --video input_videos/video_1.mp4    # Run inference using the PLAYER detection model on a specific video.
python get_weights.py --model ball --conf 0.3                            # Run inference using the BALL detection model with a lower confidence threshold (0.3).
python get_weights.py --model keypoint --video input_videos/video_2.mp4  # Run inference using the COURT KEYPOINT model to detect keypoints (e.g. lines, markers) on a basketball court.
