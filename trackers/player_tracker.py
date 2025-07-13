"""
player_tracker.py

PlayerTracker class for detecting and tracking players in video frames.

Uses a YOLO model for object detection and ByteTrack (via supervision) for multi-object tracking.
Supports batch detection and optional caching of tracks using stub files to avoid recomputation.

"""

import sys
from ultralytics import YOLO
import supervision as sv  # ByteTrack tracking library
sys.path.append("../")

from utils.stubs_utils import save_stub, read_stub


class PlayerTracker:
    def __init__(self, model_path):
        """
        Initialize the PlayerTracker with a YOLO model and ByteTrack tracker.
        """
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTrack()

    def detect_frames(self, frames, conf=0.5, batch_size=20):
        """
        Detect objects in batches of video frames using YOLO.
        """
        detections = []
        for i in range(0, len(frames), batch_size):
            batch = frames[i:i + batch_size]
            preds = self.model.predict(batch, conf=conf)
            detections.extend(preds)
        return detections

    def get_object_tracks(self, frames, read_from_stub=False, stub_path=None):
        """
        Detect and track players across video frames using ByteTrack.
        Loads cached tracks from stub if requested and available.
        """
        # Load cached tracks if available
        tracks = read_stub(read_from_stub, stub_path)
        if tracks is not None and len(tracks) == len(frames):
            return tracks

        detections = self.detect_frames(frames)
        tracks = []

        for frame_num, detection in enumerate(detections):
            class_names = detection.names
            class_id_map = {v: k for k, v in class_names.items()}

            sv_detections = sv.Detections.from_ultralytics(detection)
            tracked = self.tracker.update_with_detections(sv_detections)

            frame_tracks = {}
            for det in tracked:
                bbox = det[0].tolist()
                cls_id = det[3]
                track_id = det[4]

                # Keep only 'player' detections
                if cls_id == class_id_map.get("player"):
                    frame_tracks[track_id] = {"bbox": bbox}

            tracks.append(frame_tracks)

        # Save tracks to stub file for future use
        if stub_path:
            save_stub(stub_path, tracks)

        return tracks
