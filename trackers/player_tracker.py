"""
player_tracker.py

Tracks players in a video using a YOLO model and ByteTrack (via Supervision).
"""

from ultralytics import YOLO
import supervision as sv  # Object tracking library


class PlayerTracker:
    def __init__(self, model_path):
        """
        Initialize the tracker with a YOLO model and a ByteTrack tracker.
        """
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTrack()

    def detect_frames(self, frames):
        """
        Run YOLO detection in batches on video frames.
        """
        batch_size = 20
        detections = []

        for i in range(0, len(frames), batch_size):
            batch = frames[i:i + batch_size]
            batch_detections = self.model.predict(batch, conf=0.5)
            detections.extend(batch_detections)

        return detections

    def get_object_tracks(self, frames):
        """
        Run detection and tracking on a list of frames.
        """
        detections = self.detect_frames(frames)
        tracks = []

        class_names = self.model.names  # e.g., {0: 'ball', 1: 'player'}
        name_to_id = {v: k for k, v in class_names.items()}

        for frame_num, detection in enumerate(detections):
            det_supervision = sv.Detections.from_ultralytics(detection)
            tracked = self.tracker.update_with_detections(det_supervision)

            frame_tracks = {}
            for det in tracked:
                bbox = det[0].tolist()
                cls_id = det[3]
                track_id = det[4]

                if cls_id == name_to_id.get('player'):
                    frame_tracks[track_id] = {'box': bbox}

            tracks.append(frame_tracks)

        return tracks
