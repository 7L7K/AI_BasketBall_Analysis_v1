# Trackers Module

This folder contains object tracking implementations for video analysis, primarily focused on tracking players and balls in sports videos.

## Folder Contents
-  `player_tracker.py` : Player detection and tracking implementation   
- `ball_tracker.py`   : Ball detection and tracking implementation     
- `__init__.py`      l: To make this a Python package       

## Overview

Both trackers support:
- Batch detection of objects in video frames.
- Tracking across frames.
- Optional caching of tracking results using stub files for faster subsequent runs.

## Usage Example

```python
from trackers.player_tracker import PlayerTracker

# Initialize with YOLO model weights path
tracker = PlayerTracker("models/player_detector.pt")

# Load video frames (list of numpy arrays)
frames = load_video_frames("videos/sample.mp4")

# Get player tracks (with caching)
tracks = tracker.get_object_tracks(frames, read_from_stub=True, stub_path="stubs/player_tracks.pkl")

# Use the tracks for further processing or visualization
