"""
player_tracker.py

Defines the PlayerTracker class for detecting and tracking players in video frames.
Uses YOLO (Ultralytics) for object detection and ByteTrack (via the Supervision library)
for multi-object tracking. Supports caching via stub files.
"""

import sys
from typing import List, Dict, Optional

from ultralytics import YOLO
import supervision as sv  # Uses ByteTrack for tracking

from utils.stubs_utils import save_stub, read_stub

sys.path.append("..")


class PlayerTracker:
    def __init__(self, model_path: str):
        """
        Initializes the PlayerTracker with a YOLO model and ByteTrack tracker.
        """
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTrack()

    def detect_frames(self, frames: List, conf: float = 0.5, batch_size: int = 20):
        """
        Detects players in video frames using YOLO in batches.
        """
        detections = []
        for i in range(0, len(frames), batch_size):
            batch = frames[i:i + batch_size]
            preds = self.model.predict(batch, conf=conf)
            detections.extend(preds)
        return detections

    def get_object_tracks(
        self,
        frames: List,
        read_from_stub: bool = False,
        stub_path: Optional[str] = None
    ) -> List[Dict[int, Dict[str, List[float]]]]:
        """
        Tracks player objects across video frames using ByteTrack.
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

                if cls_id == class_id_map.get("player"):
                    frame_tracks[track_id] = {"bbox": bbox}

            tracks.append(frame_tracks)

        # Save to stub
        if stub_path:
            save_stub(stub_path, tracks)

        return tracks
