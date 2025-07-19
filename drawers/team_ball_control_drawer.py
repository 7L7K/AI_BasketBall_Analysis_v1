"""
Displays team ball possession statistics on video frames using an overlay box.
"""

import numpy as np
import cv2

class TeamBallControlDrawer:
    def __init__(self, team1_color=(0, 102, 204), team2_color=(220, 20, 60), bg_color=(245, 245, 245)):
        """
        Initializes the drawer with team and background colors.
        """
        self.team1_color = team1_color
        self.team2_color = team2_color
        self.bg_color = bg_color

    def get_team_ball_control(self, player_assignment, ball_acquisition):
        """
        Determines which team has control of the ball in each frame.
        """
        team_ball_control = []

        for player_frame, ball_owner in zip(player_assignment, ball_acquisition):
            if ball_owner == -1:
                team_ball_control.append(-1)
                continue

            team_id = player_frame.get(ball_owner, -1)
            team_ball_control.append(team_id if team_id in [1, 2] else -1)

        return np.array(team_ball_control)

    def draw(self, video_frames, player_assignment, ball_acquisition):
        """
        Draws the ball control stats overlay on all video frames.
        """
        team_ball_control = self.get_team_ball_control(player_assignment, ball_acquisition)
        output_video_frames = []

        for frame_num, frame in enumerate(video_frames):
            drawn_frame = self.draw_frame(frame.copy(), frame_num, team_ball_control)
            output_video_frames.append(drawn_frame)

        return output_video_frames

    def draw_frame(self, frame, frame_num, team_ball_control):
        """
        Draws the ball control overlay for a single frame.
        """
        overlay = frame.copy()
        font_scale = 0.75
        font_thickness = 2

        h, w = frame.shape[:2]
        rectx1 = int(w * 0.60)
        recty1 = int(h * 0.75)
        rectx2 = int(w * 0.98)
        recty2 = int(h * 0.91)

        # Draw semi-transparent background
        cv2.rectangle(overlay, (rectx1, recty1), (rectx2, recty2), self.bg_color, -1)
        alpha = 0.85
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        # Compute control percentages
        control_so_far = team_ball_control[:frame_num + 1]
        valid = control_so_far[control_so_far != -1]
        total = len(valid)

        team1_percent = np.count_nonzero(valid == 1) / total if total > 0 else 0
        team2_percent = np.count_nonzero(valid == 2) / total if total > 0 else 0

        # Text positions
        text_x = rectx1 + 15
        text_y1 = recty1 + 40
        text_y2 = recty1 + 85

        # Draw text
        cv2.putText(frame,
                    f"Team 1 Ball Control: {team1_percent * 100:.1f}%",
                    (text_x, text_y1),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale,
                    self.team1_color,
                    font_thickness)

        cv2.putText(frame,
                    f"Team 2 Ball Control: {team2_percent * 100:.1f}%",
                    (text_x, text_y2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale,
                    self.team2_color,
                    font_thickness)

        return frame
