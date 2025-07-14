"""
ball_tracker.py

This module defines a `BallTracker` class that uses a trained Ultralytics model to detect and track a 'Ball' across video frames using ByteTrack via the Supervision library, with post-processing to remove implausible detections based on motion constraints.

"""

import sys
import numpy as np
from ultralytics import YOLO
import supervision as sv  # ByteTrack-based object tracking
from utils.stubs_utils import save_stub, read_stub
import pandas as pd

sys.path.append("../")


class BallTracker:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def detect_frames(self, frames, conf=0.5, batch_size=20):
        """
        Detect objects in video frames using YOLO in batches.
        """
        detections = []
        for i in range(0, len(frames), batch_size):
            batch = frames[i:i + batch_size]
            preds = self.model.predict(batch, conf=conf)
            detections.extend(preds)
        return detections

    def get_object_tracks(self, frames, read_from_stub=False, stub_path=None):
        """
        Detect and track the 'Ball' object across frames using YOLO + ByteTrack.
        """
        # Load from stub if available
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

            for frame_detection in sv_detections:
                bbox = frame_detection[0].tolist()
                confidence = frame_detection[2]
                cls_id = frame_detection[3]

                if cls_id == class_id_map.get('Ball'):
                    if confidence > max_confidence:
                        max_confidence = confidence
                        chosen_bbox = bbox

            if chosen_bbox is not None:
                tracks[frame_num][1] = {'bbox': chosen_bbox}

        # Save results to stub
        if stub_path:
            save_stub(stub_path, tracks)

        return tracks

    def remove_wrong_detections(self, ball_positions, max_dist_per_frame=25):
        """
        Removes unrealistic ball detections based on motion constraints.
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
    

    def interpolate_ball_positions(self, ball_positions):
        """
        Fills in missing ball detections by interpolating and backfilling bounding box coordinates across frames to ensure continuous tracking.
        """
        ball_positions=[x.get(1,{}).get('bbox',{}) for x in ball_positions]
        df_ball_positions=pd.DataFrame(ball_positions)
        

        #interpolation of missing values
        df_ball_positions.interpolate()
        df_ball_positions=df_ball_positions.bfill()


        ball_positions=[{1:{"bbox":x}} for x in df_ball_positions.to_numpy().tolist() ]
        return ball_positions
