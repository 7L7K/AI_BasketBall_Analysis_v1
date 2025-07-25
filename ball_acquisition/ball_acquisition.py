import sys
from collections import deque, Counter
sys.path.append('../')
from utils.bbox_utils import measure_distance, get_center_of_bbox

class BallAquisitionDetector:
    def __init__(self):
        self.possession_threshold = 50  # max allowed distance to consider possession
        self.smoothing_window = 5       # number of frames to smooth possession detection
        self.containment_threshold = 0.8  # minimum ball containment ratio to favor possession

    def get_key_basketball_player_assignment_points(self, player_bbox, ball_center):
        """
        Compute key points around a player's bounding box relevant for ball possession.
        """
        ball_center_x, ball_center_y = ball_center
        x1, y1, x2, y2 = player_bbox
        width = x2 - x1
        height = y2 - y1

        points = []

        # Vertical alignment points
        if y1 < ball_center_y < y2:
            points.append((x1, ball_center_y))
            points.append((x2, ball_center_y))

        # Horizontal alignment points
        if x1 < ball_center_x < x2:
            points.append((ball_center_x, y1))
            points.append((ball_center_x, y2))

        # Additional key points around bbox
        points += [
            (x1 + width // 2, y1),             # top center
            (x2, y1),                         # top right
            (x1, y1),                         # top left
            (x2, y1 + height // 2),           # center right
            (x1, y1 + height // 2),           # center left
            (x1 + width // 2, y1 + height // 2),  # center
            (x2, y2),                         # bottom right
            (x1, y2),                         # bottom left
            (x1 + width // 2, y2),            # bottom center
            (x1 + width // 2, y1 + height // 3),  # mid-top center
        ]
        return points

    def calculate_ball_containment_ratio(self, player_bbox, ball_bbox):
        """
        Calculate ratio of ball area contained within player's bounding box.
        """
        px1, py1, px2, py2 = player_bbox
        bx1, by1, bx2, by2 = ball_bbox

        intersection_x1 = max(px1, bx1)
        intersection_y1 = max(py1, by1)
        intersection_x2 = min(px2, bx2)
        intersection_y2 = min(py2, by2)

        if intersection_x2 < intersection_x1 or intersection_y2 < intersection_y1:
            return 0.0

        intersection_area = (intersection_x2 - intersection_x1) * (intersection_y2 - intersection_y1)
        ball_area = (bx2 - bx1) * (by2 - by1)
        return intersection_area / ball_area

    def find_minimum_distance_to_ball(self, ball_center, player_bbox):
        """
        Find minimum Euclidean distance from ball center to key points around player bbox.
        """
        key_points = self.get_key_basketball_player_assignment_points(player_bbox, ball_center)
        return min(measure_distance(ball_center, point) for point in key_points)

    def find_best_candidate_for_possession(self, ball_center, player_tracks_frame, ball_bbox):
        """
        Find the best player candidate currently possessing the ball.
        """
        high_containment = []
        regular_distance = []

        for player_id, player_info in player_tracks_frame.items():
            player_bbox = player_info.get('bbox', [])
            if not player_bbox:
                continue

            containment = self.calculate_ball_containment_ratio(player_bbox, ball_bbox)
            min_dist = self.find_minimum_distance_to_ball(ball_center, player_bbox)

            if containment > self.containment_threshold:
                high_containment.append((player_id, min_dist))
            else:
                regular_distance.append((player_id, min_dist))

        if high_containment:
            # Select player with max distance among high containment (prefer containment)
            best_candidate = max(high_containment, key=lambda x: x[1])
            return best_candidate[0]

        if regular_distance:
            # Select closest player within threshold
            best_candidate = min(regular_distance, key=lambda x: x[1])
            if best_candidate[1] < self.possession_threshold:
                return best_candidate[0]

        return -1

    def detect_ball_possession(self, player_tracks, ball_tracks):
        """
        Detect which player has possession of the ball over frames.
        """
        num_frames = len(ball_tracks)
        possession_list = [-1] * num_frames
        candidate_buffer = deque(maxlen=self.smoothing_window)
        last_valid_player = -1
        grace_period = 3
        grace_counter = 0

        for frame_num in range(num_frames):
            ball_info = ball_tracks[frame_num].get(1, {})
            if not ball_info or not ball_info.get('bbox'):
                if grace_counter < grace_period:
                    possession_list[frame_num] = last_valid_player
                    grace_counter += 1
                continue

            ball_bbox = ball_info['bbox']
            ball_center = get_center_of_bbox(ball_bbox)

            best_player_id = self.find_best_candidate_for_possession(
                ball_center,
                player_tracks[frame_num],
                ball_bbox
            )

            candidate_buffer.append(best_player_id)

            if len(candidate_buffer) == self.smoothing_window:
                common_candidate, count = Counter(candidate_buffer).most_common(1)[0]
                if common_candidate != -1 and count >= self.smoothing_window // 2:
                    possession_list[frame_num] = common_candidate
                    last_valid_player = common_candidate
                    grace_counter = 0
                else:
                    possession_list[frame_num] = last_valid_player
                    grace_counter += 1
            else:
                possession_list[frame_num] = last_valid_player

        return possession_list
