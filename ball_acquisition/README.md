# ⚽ Ball Possession Detector

This module includes logic to estimate when a player is in possession of the ball based on bounding box geometry and proximity to the ball's center.

---

## `BallAcquisitionDetector`

A utility class to:
- Identify key points around a player's bounding box.
- Detect whether the ball is close enough to infer possession.

### Example Usage:

```python
from ball_acquisition_detector import BallAcquisitionDetector

detector = BallAcquisitionDetector()
key_points = detector.get_key_ball_player_assignment_points(player_bbox, ball_center)
