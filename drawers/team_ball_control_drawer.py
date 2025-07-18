# team_ball_control_drawer.py

"""
Displays team ball possession statistics on video frames using an overlay box.
"""

import numpy as np
import cv2

class TeamBallControlDrawer:
    def __init__(self):
        # Colors in BGR
        self.bg_color = (245, 245, 245)         # Light gray background
        self.team1_color = (0, 102, 204)        # Blue for Team 1
        self.team2_color = (220, 20, 60)        # Crimson red for Team 2
        self.text_color = (0, 0, 0)             # Black text

    def get_team_ball_control(self, player_assignment, ball_acquisition):
        """
        Determines which team has control of the ball in each frame.
        """
        team_ball_control = []

        for player_assignment_frame, ball_acquisition_frame in zip(player_assignment, ball_acquisition):
            if ball_acquisition_frame == -1:
                team_ball_control.append(-1)
                continue

            team_id = player_assignment_frame.get(ball_acquisition_frame, -1)
            if team_id in [1, 2]:
                team_ball_control.append(team_id)
            else:
                team_ball_control.append(-1)

        return np.array(team_ball_control)

    def draw(self, video_frames, player_assignment, ball_acquisition):
        """
        Draws team ball control overlay on video frames.
        """
        team_ball_control = self.get_team_ball_control(player_assignment, ball_acquisition)
        output_video_frames = []

        for frame_num, frame in enumerate(video_frames):
            if frame_num == 0:
                output_video_frames.append(frame)
                continue
            frame_drawn = self.draw_frame(frame, frame_num, team_ball_control)
            output_video_frames.append(frame_drawn)

        return output_video_frames

    def draw_frame(self, frame, frame_num, team_ball_control):
        """
        Draws the ball control overlay for a single frame.
        """
        overlay = frame.copy()
        font_scale = 0.75
        font_thickness = 2

        frame_height, frame_width = overlay.shape[:2]
        rectx1 = int(frame_width * 0.60)
        recty1 = int(frame_height * 0.75)
        rectx2 = int(frame_width * 0.98)
        recty2 = int(frame_height * 0.91)

        # Draw semi-transparent background rectangle
        cv2.rectangle(overlay, (rectx1, recty1), (rectx2, recty2), self.bg_color, -1)
        alpha = 0.85
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        # Calculate control percentages
        team_ball_control_till_now = team_ball_control[:frame_num + 1]
        total = np.count_nonzero(team_ball_control_till_now != -1)

        if total == 0:
            team1_percent = team2_percent = 0
        else:
            team1_frames = np.count_nonzero(team_ball_control_till_now == 1)
            team2_frames = np.count_nonzero(team_ball_control_till_now == 2)
            team1_percent = team1_frames / total
            team2_percent = team2_frames / total

        # Text positions
        text_x = rectx1 + 15
        text_y1 = recty1 + 40
        text_y2 = recty1 + 85

        # Draw text with team-specific color
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
