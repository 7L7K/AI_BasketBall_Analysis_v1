# 🖍️ Drawers

This folder contains modules responsible for **visualizing tracking results** on video frames. These modules add intuitive and minimalistic overlays to help highlight players and the ball in a sports video, especially for basketball analytics.

## 📁 Contents

- `player_tracks_drawer.py` : Draws elegant **ellipses** under each tracked player, and overlays their unique **track ID** in a filled rectangle above their position.  
- `ball_tracks_drawer.py` : Draws a **green triangle pointer** to indicate the detected position of the ball in each frame.

- `utils.py`
Helper functions used for drawing: `draw_ellipse(...)`: Draws an anti-aliased ellipse + optional label and  `draw_triangle(...)`: Draws a triangle marker at a given location.


## ✅ Example Usage

Once tracking is complete:

```python
from drawers.player_tracks_drawer import PlayerTracksDrawer
from drawers.ball_tracks_drawer import BallTracksDrawer

player_drawer = PlayerTracksDrawer()
ball_drawer = BallTracksDrawer()

player_frames = player_drawer.draw(video_frames, player_tracks)
final_frames = ball_drawer.draw(player_frames, ball_tracks)
