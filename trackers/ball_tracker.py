"""
ball_tracker.py

Defines a `BallTracker` class that uses a trained YOLO model (Ultralytics)
to detect and track a ball across video frames using ByteTrack via the
Supervision library. Includes post-processing to discard implausible detections
and interpolate missing ones.
"""

import sys
from typing import List, Dict, Optional

import numpy as np
import pandas as pd
from ultralytics import YOLO
import supervision as sv  # Uses ByteTrack for tracking

from utils.stubs_utils import save_stub, read_stub

sys.path.append("..")


class BallTracker:
    def __init__(self, model_path: str):
        """
        Initializes the YOLO-based ball tracker.

        Args:
            model_path (str): Path to the trained YOLO model.
        """
        self.model = YOLO(model_path)

    def detect_frames(self, frames: List, conf: float = 0.5, batch_size: int = 20):
        """
        Detects objects in video frames using YOLO in batches.
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
        Detects and tracks the 'Ball' object across frames using YOLO + ByteTrack.
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
            tracks.append({})
            chosen_bbox = None
            max_confidence = 0

            for detection_item in sv_detections:
                bbox = detection_item[0].tolist()
                confidence = detection_item[2]
                cls_id = detection_item[3]

                if cls_id == class_id_map.get("Ball"):
                    if confidence > max_confidence:
                        max_confidence = confidence
                        chosen_bbox = bbox

            if chosen_bbox is not None:
                tracks[frame_num][1] = {'bbox': chosen_bbox}

        if stub_path:
            save_stub(stub_path, tracks)

        return tracks

    def remove_wrong_detections(
        self, 
        ball_positions: List[Dict[int, Dict[str, List[float]]]], 
        max_dist_per_frame: float = 25
    ) -> List[Dict[int, Dict[str, List[float]]]]:
        """
        Removes implausible ball detections based on motion constraints.
        """
        last_good_frame_index = -1

        for i in range(len(ball_positions)):
            current_bbox = ball_positions[i].get(1, {}).get('bbox', [])
            if not current_bbox:
                continue

            if last_good_frame_index == -1:
                last_good_frame_index = i
                continue

            last_bbox = ball_positions[last_good_frame_index].get(1, {}).get('bbox', [])
            frame_gap = i - last_good_frame_index
            allowed_distance = max_dist_per_frame * frame_gap

            if np.linalg.norm(np.array(current_bbox[:2]) - np.array(last_bbox[:2])) > allowed_distance:
                ball_positions[i] = {}
            else:
                last_good_frame_index = i

        return ball_positions

    def interpolate_ball_positions(
        self, 
        ball_positions: List[Dict[int, Dict[str, List[float]]]]
    ) -> List[Dict[int, Dict[str, List[float]]]]:
        """
        Fills in missing ball detections by interpolating and backfilling bounding boxes.
        """
        bboxes = [frame.get(1, {}).get('bbox', None) for frame in ball_positions]

        # Check if we have at least one valid bbox
        if all(b is None for b in bboxes):
            print("No valid ball detections to interpolate.")
            return [{} for _ in ball_positions]

        df = pd.DataFrame(bboxes)

        # Interpolate and backfill to fill NaNs
        df = df.interpolate(limit_direction='both').bfill()

        # Rebuild structured output
        interpolated = []
        for row in df.to_numpy().tolist():
            if any(pd.isna(coord) for coord in row):
                interpolated.append({})
            else:
                interpolated.append({1: {'bbox': row}})
        return interpolated
