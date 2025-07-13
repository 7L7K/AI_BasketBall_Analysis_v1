"""
player_tracker.py

Tracks players in a video using a YOLO model and ByteTrack (via Supervision).
"""

import sys
import pickle
from ultralytics import YOLO
import supervision as sv  # ByteTrack-based tracking
sys.path.append("../")

from utils import save_stub, read_stub


class PlayerTracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTrack()

    def detect_frames(self, frames, conf=0.5, batch_size=20):
        """
        Detect objects in frames using YOLO model in batches.
        """
        detections = []
        for i in range(0, len(frames), batch_size):
            batch = frames[i:i + batch_size]
            preds = self.model.predict(batch, conf=conf)
            detections.extend(preds)
        return detections

    def get_object_tracks(self, frames, read_from_stub=False, stub_path=None):
        """
        Detect and track 'player' objects across frames. 
        Optionally load/save from stub to avoid recomputation.
        """
        tracks = read_stub(read_from_stub, stub_path)
        if tracks is not None and len(tracks) == len(frames):
            return tracks

        detections = self.detect_frames(frames)
        tracks = []

        for frame_num, detection in enumerate(detections):
            class_names = detection.names
            class_id_map = {v: k for k, v in class_names.items()}
            
            sv_detections = sv.Detections.from_ultralytics(detection)
            tracked_detections = self.tracker.update_with_detections(sv_detections)

            tracks.append({})
            for det in tracked_detections:
                bbox = det[0].tolist()
                cls_id = det[3]
                track_id = det[4]

                # Focus only on players
                if cls_id == class_id_map.get("player"):
                    tracks[frame_num][track_id] = {"box": bbox}

        if stub_path:
            save_stub(stub_path, tracks)

        return tracks
