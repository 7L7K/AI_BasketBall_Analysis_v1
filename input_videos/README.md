# Input Videos

- This folder contains the **raw input videos** used for player and ball detection and tracking in the project.
- The videos in this folder serve as input data for the tracking pipeline, which processes them to detect and track objects (such as players or balls) using YOLO and ByteTrack models.
- Videos should be in formats supported by OpenCV and YOLO (e.g., `.mp4`, `.avi`).

A valid setup might look like this:
```python
frames = read_video("input_videos/video_1.mp4")

