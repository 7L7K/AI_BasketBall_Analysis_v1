"""
ball_tracks_drawer.py

Draws visual markers for ball positions on video frames.
Uses green triangle pointers to indicate ball locations.
"""

from typing import List, Dict, Any
from .utils import draw_triangle


class BallTracksDrawer:
    """
    Class for drawing ball position markers on video frames using triangle pointers.
    """

    def __init__(self, pointer_color: tuple = (0, 255, 0)):
        """
        Initializes the drawer with the color for the ball pointer.
        """
        self.ball_pointer_color = pointer_color

    def draw(
        self, 
        video_frames: List[Any], 
        tracks: List[Dict[int, Dict[str, Any]]]
    ) -> List[Any]:
        """
        Draws triangle markers for ball positions on each frame.
        """
        output_video_frames = []

        for frame_num, frame in enumerate(video_frames):
            frame_copy = frame.copy()
            ball_dict = tracks[frame_num]

            for track in ball_dict.values():
                bbox = track.get('bbox')
                if bbox:
                    frame_copy = draw_triangle(frame_copy, bbox, color=self.ball_pointer_color)

            output_video_frames.append(frame_copy)

        return output_video_frames
