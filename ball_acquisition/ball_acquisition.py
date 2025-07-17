"""
ball_acquisition_detector.py

Detects potential ball possession by identifying whether the ball lies within
a player's bounding box or close to key points around it.
"""

class BallAcquisitionDetector:
    def __init__(self):
        self.possession_threshold = 50       # Distance threshold for ball-player assignment
        self.min_frames = 11                 # Minimum number of frames to consider possession
        self.containment = 0.8               # Placeholder for future containment metric logic

    def get_key_ball_player_assignment_points(self, player_bbox, ball_center):
        """
        Generate key spatial points on the player bounding box to check proximity to the ball.
        """
        ball_center_x, ball_center_y = ball_center
        x1, y1, x2, y2 = player_bbox
        width = x2 - x1
        height = y2 - y1

        output_points = []

        # Horizontal or vertical alignment with the ball center
        if y1 < ball_center_y < y2:
            output_points.append((x1, ball_center_y))
            output_points.append((x2, ball_center_y))
        if x1 < ball_center_x < x2:
            output_points.append((ball_center_x, y1))
            output_points.append((ball_center_x, y2))

        # Add corners and midpoints of the bounding box
        output_points += [
            (x1, y1),           # Top-left
            (x2, y1),           # Top-right
            (x1, y2),           # Bottom-left
            (x2, y2),           # Bottom-right
            (x1, y1 + height // 2),       # Left-middle
            (x2, y1 + height // 2),       # Right-middle
            (x1 + width // 2, y1),        # Top-middle
            (x1 + width // 2, y2)         # Bottom-middle
        ]

        return output_points
