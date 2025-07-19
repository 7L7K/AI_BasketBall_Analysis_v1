from ultralytics import YOLO
import sys
sys.path.append("../") 
from utils import read_stub, save_stub

class CourtKeypointDetection:
    def __init__(self, model_path: str):
        """
        Initialize the YOLO model for keypoint detection.
        """
        self.model = YOLO(model_path)

    def get_court_keypoints(self, frames, conf_threshold=0.5, batch_size=20, read_from_stub=False, stub_path=None):
        """
        Predict court keypoints on a list of frames.
        """
        court_keypoints = read_stub(read_from_stub, stub_path)
        if court_keypoints is not None :
          if len(court_keypoints)==len(frames):
            return court_keypoints
          else:
            for i in range(0, len(frames), batch_size):
                batch = frames[i:i+batch_size]
                detections_batch = self.model.predict(batch, conf=conf_threshold)
                for detection in detections_batch:
                    court_keypoints.append(detection.keypoints)
        save_stub(stub_path, court_keypoints)
        return court_keypoints
