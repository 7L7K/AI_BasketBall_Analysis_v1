"""
video_utils.py

Simple utilities to read and save videos using OpenCV.
"""

import cv2
import os


def read_video(video_path):
    """
    Reads a video and returns its frames as a list.
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


def save_video(frames, output_path, fps=24.0):
    """
    Saves a list of frames as a video.
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
