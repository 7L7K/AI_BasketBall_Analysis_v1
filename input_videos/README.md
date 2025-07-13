# Input Videos

This folder contains the **raw input videos** used for player and ball detection and tracking in the project.

## Purpose

The videos in this folder serve as input data for the tracking pipeline, which processes them to detect and track objects (such as players or balls) using YOLO and ByteTrack models.

## Format & Naming

- Videos should be in formats supported by OpenCV and YOLO (e.g., `.mp4`, `.avi`).
- Use meaningful names (e.g., `video_1.mp4`, `nba_match_clip.mp4`) to easily distinguish clips.
- Ensure frame resolution and quality are suitable for YOLO detection (at least 720p recommended).

## Example

A valid setup might look like this:
```python
frames = read_video("input_videos/video_1.mp4")

