# 🧢 Team Assigner Module

This module contains the logic for automatically assigning basketball players to their teams based on jersey color, using the [Fashion CLIP](https://huggingface.co/patrickjohncyh/fashion-clip) model from Hugging Face.

It is used as part of the larger **AI-Powered Basketball Analysis System** to differentiate between teams across video frames.

---

## 📁 Contents

- `team_assigner.py` — Main class `TeamAssigner` with methods for loading the model, predicting jersey colors, and assigning team IDs to players across frames.
- `__init__.py` — Empty init file to make this folder a Python module.

---

## 🚀 Features

- 🎨 **Zero-shot classification** with Fashion CLIP  
- 🧠 Maintains player-team associations across frames  
- 💾 Optional caching via `read_stub` / `save_stub` to speed up repeated runs  
- 🔄 Resets predictions every 50 frames for robustness

---

## 🧱 Usage Example

```python
from scripts.team_assigner import TeamAssigner

assigner = TeamAssigner("white shirt", "dark blue shirt")
team_assignments = assigner.get_player_team_across_frames(video_frames, player_tracks, read_from_stub=True, stub_path="cache/team_labels.pkl")
