"""
get_weights.py

Run inference using trained YOLO models:
- Player and ball detection (YOLOv5 or YOLOv8)
- Court keypoint detection (YOLOv8-pose)

Usage:
    python get_weights.py --model player
    python get_weights.py --model ball
    python get_weights.py --model keypoint
"""

import argparse
from ultralytics import YOLO
import os
import sys

def main(model_name: str, input_video: str, conf: float):
    model_paths = {
        "player": "models/player_detector.pt",
        "ball": "models/ball_detector.pt",
        "keypoint": "models/keypoint_court.pt"
    }

    if model_name not in model_paths:
        raise ValueError(f"Unknown model: {model_name}. Choose from {list(model_paths.keys())}")

    model_path = model_paths[model_name]

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Model file not found at: {model_path}")

    if not os.path.exists(input_video):
        raise FileNotFoundError(f"❌ Input video not found: {input_video}")

    print(f"🔍 Running inference using '{model_path}' on '{input_video}' with conf={conf}")

    model = YOLO(model_path)

    results = model.predict(
        source=input_video,
        save=True,
        imgsz=640,
        conf=conf,
        show=False
    )

    print(f"\n Inference complete. Output saved in: {results[0].save_dir}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run inference using YOLOv5 or YOLOv8 model.")
    parser.add_argument("--model", choices=["player", "ball", "keypoint"], required=True,
                        help="Choose which model to use for inference")
    parser.add_argument("--video", default="input_videos/video_1.mp4",
                        help="Path to input video file")
    parser.add_argument("--conf", type=float, default=0.25,
                        help="Confidence threshold for predictions")
    args = parser.parse_args()

    main(args.model, args.video, args.conf)
