# ball_acquisition_detector.py

"""
Detects potential ball possession by identifying whether the ball lies within
a player's bounding box or close to key points around it.
"""

import sys
sys.path.append("../")
from utils import measure_distance, get_center_bbox


class BallAcquisitionDetector:
    def __init__(self):
        self.possession_threshold = 50       # Distance threshold for ball-player assignment
        self.min_frames = 11                 # Minimum number of frames to consider possession
        self.containment_threshold = 0.8     # Placeholder for future containment metric logic

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
            (x1, y1),                         # Top-left
            (x2, y1),                         # Top-right
            (x1, y2),                         # Bottom-left
            (x2, y2),                         # Bottom-right
            (x1, y1 + height // 2),           # Left-middle
            (x2, y1 + height // 2),           # Right-middle
            (x1 + width // 2, y1),            # Top-middle
            (x1 + width // 2, y2)             # Bottom-middle
        ]

        return output_points

    def find_minimum_distance_to_ball(self, ball_center, player_bbox):
        """
        Compute the minimum distance from the ball center to key points around a player's bounding box.
        """
        key_points = self.get_key_ball_player_assignment_points(player_bbox, ball_center)
        return min(
            ((px - ball_center[0]) ** 2 + (py - ball_center[1]) ** 2) ** 0.5
            for px, py in key_points
        )

    def calculate_ball_containment_ratio(self, player_bbox, ball_bbox):
        """
        Calculates the area of intersection between ball and player bounding boxes
        as a fraction of the ball area.
        """
        x1_p, y1_p, x2_p, y2_p = player_bbox
        x1_b, y1_b, x2_b, y2_b = ball_bbox

        x_left = max(x1_p, x1_b)
        y_top = max(y1_p, y1_b)
        x_right = min(x2_p, x2_b)
        y_bottom = min(y2_p, y2_b)

        if x_right < x_left or y_bottom < y_top:
            return 0.0

        intersection_area = (x_right - x_left) * (y_bottom - y_top)
        ball_area = (x2_b - x1_b) * (y2_b - y1_b)

        if ball_area == 0:
            return 0.0

        return intersection_area / ball_area

    def find_best_candidate_for_possession(self, ball_center, player_tracks_frame, ball_bbox):
        high_containment_players = []
        regular_distance_players = []

        for player_id, player_info in player_tracks_frame.items():
            player_bbox = player_info.get("bbox", [])
            if not player_bbox:
                continue

            containment = self.calculate_ball_containment_ratio(player_bbox, ball_bbox)
            min_distance = self.find_minimum_distance_to_ball(ball_center, player_bbox)

            if containment > self.containment_threshold:
                high_containment_players.append((player_id, containment))
            else:
                regular_distance_players.append((player_id, min_distance))

        if high_containment_players:
            best_candidate = max(high_containment_players, key=lambda x: x[1])
            return best_candidate[0]

        if regular_distance_players:
            best_distance = min(regular_distance_players, key=lambda x: x[1])
            if best_distance[1] < self.possession_threshold:
                return best_distance[0]

        return -1

    def detect_ball_possession(self, player_tracks, ball_tracks):
        """
        Given all frames, assigns possession to a player for each frame
        based on proximity or containment.
        """
        num_frames = len(ball_tracks)
        possession_list = [-1] * num_frames
        consecutive_possession_count = {}

        for frame_num in range(num_frames):
            ball_info = ball_tracks[frame_num].get(1, {})
            if not ball_info:
                continue

            ball_bbox = ball_info.get("bbox", [])
            if not ball_bbox:
                continue

            ball_center = get_center_bbox(ball_bbox)
            player_frame_info = player_tracks[frame_num]
            best_player_id = self.find_best_candidate_for_possession(ball_center, player_frame_info, ball_bbox)

            if best_player_id != -1:
                num_consecutive_frames = consecutive_possession_count.get(best_player_id, 0) + 1
                consecutive_possession_count = {best_player_id: num_consecutive_frames}

                if num_consecutive_frames >= self.min_frames:
                    possession_list[frame_num] = best_player_id
                else:
                    possession_list[frame_num] = -1
            else:
                consecutive_possession_count = {}

        return possession_list
