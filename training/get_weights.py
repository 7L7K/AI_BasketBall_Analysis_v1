"""
get_weights.py

Run inference with YOLOv5 on a given video using either the player or ball detector.

Usage:
    python get_weights.py --model player
    python get_weights.py --model ball
"""

import argparse
from ultralytics import YOLO
import os

def main(model_name):
    model_path = f"models/{model_name}_detector.pt"
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found: {model_path}")

    input_video = "input_videos/video_1.mp4"
    print(f"🔍 Running inference using '{model_path}' on '{input_video}'")

    model = YOLO(model_path)
    results = model.predict(input_video, save=True)

    print("Inference complete. Predictions:")
    for box in results[0].boxes:
        print(box)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run YOLOv5 inference on video input.")
    parser.add_argument("--model", choices=["player", "ball"], required=True, help="Choose model: 'player' or 'ball'")
    args = parser.parse_args()

    main(args.model)
