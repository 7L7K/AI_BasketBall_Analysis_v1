"""
player_tracks_drawer.py

Draws tracked player positions on video frames using ellipses.
"""

import cv2
from .utils import draw_ellipse 


class PlayerTracksDrawer:
    def __init__(self, team1_color=[255,245,238],team2_color=[128,0,0]):
        self.default_player_team_id=1
        self.team1_color=team1_color
        self.team2_color=team2_color
        

    def draw(self, video_frames, tracks, player_assignment):
        """
        Draws ellipses on player positions for each frame.
        """
        output_video_frames = []

        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()
            player_dict = tracks[frame_num]

            player_assignment_for_frame=player_assignment[frame_num]
            for track_id, player in player_dict.items():
                team_id=player_assignment_for_frame.get(track_id,self.default_player_team_id)
                if team_id ==1:
                    color=self.team1_color
                else:
                    color=self.team2_color
                bbox = player['box']
                frame = draw_ellipse(frame, bbox, color=color) 

            output_video_frames.append(frame)

        return output_video_frames
