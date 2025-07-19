import cv2
import numpy as np

class PassInterceptionDrawer:
    def __init__(self, team1_color=(255, 0, 0), team2_color=(0, 0, 255), bg_color=(20, 20, 20)):
        """
        Initializes the drawer with team and background colors.
        """
        self.team1_color = team1_color
        self.team2_color = team2_color
        self.bg_color = bg_color

    def draw(self, video_frames, passes, interceptions):
        """
        Draws pass and interception stats onto each video frame.
        
        Args:
            video_frames (list): List of video frames (BGR images).
            passes (list): List containing pass detection info per frame.
            interceptions (list): List containing interception info per frame.

        Returns:
            list: Video frames with overlaid stats.
        """
        output_video_frames = []

        for frame_num, frame in enumerate(video_frames):
            drawn_frame = self.draw_frame(frame.copy(), frame_num, passes, interceptions)
            output_video_frames.append(drawn_frame)

        return output_video_frames

    def get_stats(self, passes, interceptions, until_frame=None):
        """
        Computes the number of passes and interceptions per team.

        Args:
            passes (list): List of team pass events per frame.
            interceptions (list): List of team interception events per frame.
            until_frame (int): Frame number to compute stats up to (exclusive). If None, uses entire list.

        Returns:
            tuple: (team1_passes, team2_passes, team1_interceptions, team2_interceptions)
        """
        if until_frame is None:
            until_frame = len(passes)

        team1_passes = sum(1 for i in range(until_frame) if passes[i] == 1)
        team2_passes = sum(1 for i in range(until_frame) if passes[i] == 2)
        team1_interceptions = sum(1 for i in range(until_frame) if interceptions[i] == 1)
        team2_interceptions = sum(1 for i in range(until_frame) if interceptions[i] == 2)

        return team1_passes, team2_passes, team1_interceptions, team2_interceptions

    def draw_frame(self, frame, frame_num, passes, interceptions):
        """
        Overlays pass/interception statistics for the current frame.

        Args:
            frame (np.ndarray): The video frame.
            frame_num (int): Current frame number.
            passes (list): Passes list.
            interceptions (list): Interceptions list.

        Returns:
            np.ndarray: Annotated frame.
        """
        overlay = frame.copy()
        font_scale = 0.75
        font_thickness = 2

        h, w = frame.shape[:2]
        rectx1 = int(w * 0.16)
        recty1 = int(h * 0.75)
        rectx2 = int(w * 0.55)
        recty2 = int(h * 0.91)

        text_x = rectx1 + 15
        text_y1 = recty1 + 40
        text_y2 = recty1 + 80
        text_y3 = recty1 + 120
        text_y4 = recty1 + 160

        # Draw semi-transparent background
        cv2.rectangle(overlay, (rectx1, recty1), (rectx2, recty2), self.bg_color, -1)
        alpha = 0.85
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        # Get stats up to this frame
        t1_passes, t2_passes, t1_interceptions, t2_interceptions = self.get_stats(passes, interceptions, frame_num)

        # Overlay text
        cv2.putText(frame, f"Team 1 Passes: {t1_passes}", (text_x, text_y1),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, self.team1_color, font_thickness)

        cv2.putText(frame, f"Team 2 Passes: {t2_passes}", (text_x, text_y2),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, self.team2_color, font_thickness)

        cv2.putText(frame, f"Team 1 Interceptions: {t1_interceptions}", (text_x, text_y3),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, self.team1_color, font_thickness)

        cv2.putText(frame, f"Team 2 Interceptions: {t2_interceptions}", (text_x, text_y4),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, self.team2_color, font_thickness)

        return frame
