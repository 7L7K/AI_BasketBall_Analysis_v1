# 🖍️ Drawers

This folder contains modules responsible for **visualizing tracking results** on video frames. These modules add intuitive and minimalistic overlays to help highlight players and the ball in a sports video, especially for basketball analytics.

## 📁 Contents

- `player_tracks_drawer.py` : Draws elegant **ellipses** under each tracked player, and overlays their unique **track ID** in a filled rectangle above their position.  
- `ball_tracks_drawer.py` : Draws a **green triangle pointer** to indicate the detected position of the ball in each frame.
- `team_ball_control_drawer.py` : Displays a **clean overlay box** on each video frame showing **ball possession statistics** between the two teams over time. It calculates cumulative control percentages and updates them in real-time with visually distinct colors for **Team 1 (blue)** and **Team 2 (crimson)**.
- `utils.py` : Helper functions used for drawing: `draw_ellipse(...)`: Draws an anti-aliased ellipse + optional label and  `draw_triangle(...)`: Draws a triangle marker at a given location.


## ✅ Example Usage

Once tracking is complete:

```python
from drawers.player_tracks_drawer import PlayerTracksDrawer
from drawers.ball_tracks_drawer import BallTracksDrawer
from drawers.team_ball_control_drawer import TeamBallControlDrawer

# Initialize drawers
player_drawer = PlayerTracksDrawer()
ball_drawer = BallTracksDrawer()
team_control_drawer = TeamBallControlDrawer()

# Step 1: Draw player ellipses
player_frames = player_drawer.draw(video_frames, player_tracks, player_assignments, ball_acquisition)

# Step 2: Draw ball triangle
combined_frames = ball_drawer.draw(player_frames, ball_tracks)

# Step 3: Overlay team ball possession percentages
final_frames = team_control_drawer.draw(combined_frames, player_assignments, ball_acquisition)

