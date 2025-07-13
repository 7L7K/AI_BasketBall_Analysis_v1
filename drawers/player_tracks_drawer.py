"""
player_tracks_drawer.py

Draws tracked player positions on video frames using ellipses.
"""

import cv2
from .utils import draw_ellipse 


class PlayerTracksDrawer:
    def __init__(self):
        pass

    def draw(self, video_frames, tracks):
        """
        Draws ellipses on player positions for each frame.
        """
        output_video_frames = []

        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()
            player_dict = tracks[frame_num]

            for track_id, player in player_dict.items():
                bbox = player['box']
                frame = draw_ellipse(frame, bbox, color=(0, 0, 255))  # Red ellipse

            output_video_frames.append(frame)

        return output_video_frames
