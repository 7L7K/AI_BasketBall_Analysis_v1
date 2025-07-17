"""
video_utils.py

Utility functions for reading and saving videos using OpenCV.
"""

import cv2
import os
from typing import List


def read_video(video_path: str) -> List:
    """
    Reads a video file and returns its frames as a list of numpy arrays.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    cap = cv2.VideoCapture(video_path)
    frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    cap.release()
    return frames


def save_video(frames: List, output_path: str, fps: float = 24.0) -> None:
    """
    Saves a list of video frames to a video file.
    """
    if not frames:
        raise ValueError("Frame list is empty. Cannot save video.")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    height, width = frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in frames:
        out.write(frame)

    out.release()
    print(f"Video saved to {output_path}")
