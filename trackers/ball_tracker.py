"""
ball_tracker.py

BallTracker class for detecting and tracking a ball in video frames using YOLO and ByteTrack.

"""

from ultralytics import YOLO
import sys
import supervision as sv  # Tracking library using ByteTrack
sys.path.append("../")

from utils.stubs_utils import save_stub, read_stub


class BallTracker:
    def __init__(self, model_path):
        """
        Initialize the BallTracker with a YOLO model.
        
        Args:
            model_path (str): Path to the YOLO model weights.
        """
        self.model = YOLO(model_path)

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
        Detect and track the ball across video frames.
        Optionally read/save results from/to a stub file to avoid recomputation.
        
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
            chosen_bbox = None
            max_confidence = 0
            tracks.append({})

            for det in sv_detections:
                bbox = det[0].tolist()
                cls_id = det[3]
                confidence = det[2]

                # Select the ball detection with the highest confidence
                if cls_id == class_id_map.get('Ball') and confidence > max_confidence:
                    max_confidence = confidence
                    chosen_bbox = bbox

            if chosen_bbox is not None:
                tracks[frame_num][1] = {'bbox': chosen_bbox}

        # Save tracks to stub file for future reuse
        if stub_path:
            save_stub(stub_path, tracks)

        return tracks

