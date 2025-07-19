# Passes and Interceptions Detector

This module provides tools to **analyze ball possession changes** in a sports video to detect **passes** and **interceptions** based on tracking data.

---

## 🔁 Pass Detection

A **pass** is detected when:

- The ball changes possession from one player to another.
- **Both players belong to the same team.**

---

## ⛔ Interception Detection

An **interception** is detected when:

- The ball changes possession from one player to another.
- **Players belong to different teams.**

---

## ✅ Example Usage

```python
from analysis.pass_and_interception_detector import PassAndInterceptionDetector

detector = PassAndInterceptionDetector()

# `ball_acquisition` contains player IDs (or -1 if no one has the ball)
# `player_assignment` is a list of dicts per frame: {player_id: team_id}

passes = detector.detect_passes(ball_acquisition, player_assignment)
interceptions = detector.detect_interceptions(ball_acquisition, player_assignment)

# Example: Log pass and interception frames
for frame_num, team in enumerate(passes):
    if team != -1:
        print(f"Pass by Team {team} at frame {frame_num}")

for frame_num, team in enumerate(interceptions):
    if team != -1:
        print(f"Interception by Team {team} at frame {frame_num}")
