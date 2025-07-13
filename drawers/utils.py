import cv2
import sys
sys.path.append("../")
from utils import get_center_bbox, get_width_bbox

def draw_ellipse(frame, bbox, color, track_id=None):
    """
    Draws an anti-aliased ellipse under the player, along with their track ID.
    """
    # Get foot position and ellipse dimensions
    y2 = int(bbox[3])  # Bottom of the bbox (player's feet)
    x_center, _ = get_center_bbox(bbox)
    width = get_width_bbox(bbox)

    # Draw anti-aliased ellipse
    cv2.ellipse(
        frame,
        center=(x_center, y2),
        axes=(int(width), int(0.35 * width)),
        angle=0,
        startAngle=-45,
        endAngle=235,
        color=color,
        thickness=2,
        lineType=cv2.LINE_AA
    )

    # Draw track ID (if available)
    if track_id is not None:
        rect_width = 40
        rect_height = 20

        x1_rect = x_center - rect_width // 2
        y1_rect = y2 - rect_height // 2 + 15
        x2_rect = x_center + rect_width // 2
        y2_rect = y2 + rect_height // 2 + 15

        # Filled rectangle
        cv2.rectangle(
            frame,
            (x1_rect, y1_rect),
            (x2_rect, y2_rect),
            color,
            thickness=cv2.FILLED
        )

        # Adjust text x-position if ID is large
        x_text = x1_rect + 12
        if track_id > 99:
            x_text -= 10

        # Draw ID as black text
        cv2.putText(
            frame,
            str(track_id),
            (x_text, y1_rect + 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 0),
            thickness=2,
            lineType=cv2.LINE_AA
        )

    return frame
