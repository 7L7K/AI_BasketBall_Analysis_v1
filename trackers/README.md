# 🛰️ Trackers

This folder contains object tracking implementations for video analysis, primarily focused on tracking players and balls in sports videos.

---

## 📄 Files

- 🎽 `player_tracker.py` – Player detection and tracking using YOLO + ByteTrack  
- ⚽ `ball_tracker.py` – Ball detection and tracking with YOLO + ByteTrack  
- 📦 `__init__.py` – Marks the folder as a Python package

---

## 🚀 Usage Example

```python
from trackers.player_tracker import PlayerTracker
from utils.video_utils import read_video

# Initialize tracker with YOLO model weights path
tracker = PlayerTracker("models/player_detector.pt")

# Load video frames (list of numpy arrays)
frames = read_video("videos/sample.mp4")

# Get player tracks (with caching)
tracks = tracker.get_object_tracks(
    frames, 
    read_from_stub=True, 
    stub_path="stubs/player_tracks.pkl"
)
