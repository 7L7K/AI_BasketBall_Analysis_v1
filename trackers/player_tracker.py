"""
player_tracker.py

Uses a YOLOv5 model with ByteTrack to detect and track players across video frames.
"""

from ultralytics import YOLO
import supervision as sv  # Tracking library


class PlayerTracker:
    def __init__(self, model_path):
        """
        Initialize the player tracker with a YOLO model and ByteTrack.
        """
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTrack()

    def detect_frames(self, frames):
        """
        Runs object detection on a list of frames.
        """
        batch_size = 20  # For efficient batch processing
        all_detections = []

        for i in range(0, len(frames), batch_size):
            batch = frames[i:i + batch_size]
            detections = self.model.predict(batch, conf=0.5)
            all_detections.extend(detections)

        return all_detections

