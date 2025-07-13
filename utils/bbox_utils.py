"""
bbox_utils.py

Utility functions for working with bounding boxes.
"""


def get_center_bbox(bbox):
    """
    Compute the center point of a bounding box.
    """
    x1, y1, x2, y2 = bbox
    x_center = int((x1 + x2) / 2)
    y_center = int((y1 + y2) / 2)
    return x_center, y_center


def get_width_bbox(bbox):
    """
    Compute the width of a bounding box.
    """
    x1, _, x2, _ = bbox
    return x2 - x1
