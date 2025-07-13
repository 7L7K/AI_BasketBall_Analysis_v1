import cv2
import sys
sys.path.append("../")
from utils import get_center_bbox, get_width_bbox

def draw_ellipse(frame, bbox, color, track_id=None):
    """
    Draw an elegant ellipse under a player using their bounding box.
    """
    y2 = int(bbox[3])  # Player's foot position
    x_center, _ = get_center_bbox(bbox)
    width = get_width_bbox(bbox)

    cv2.ellipse(
        frame,
        center=(x_center, y2),
        axes=(int(width), int(0.35 * width)),
        angle=0,
        startAngle=-45,
        endAngle=235,
        color=color,
        thickness=2,
        lineType=cv2.LINE_AA  # Anti-aliased for smooth rendering
    )
