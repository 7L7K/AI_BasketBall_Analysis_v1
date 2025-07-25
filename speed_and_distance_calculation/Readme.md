# ⚡ Speed and Distance Calculator ⚡

This module provides tools to calculate players' movement distances and speeds in real-world units from video frames. 🏃‍♂️📏

## Features

-  Converts player pixel coordinates to meters based on known field dimensions.
-  Calculates per-frame distances traveled by each player.
-  Computes player speeds over a sliding window of frames (default: last 5 frames).
-  Supports variable video frame rates (fps).

##  Usage

```pythom
# 1. Initialize the `SpeedAndDistanceCalculator` with video resolution and real-world field size:
calculator = SpeedAndDistanceCalculator(width_in_pixels, height_in_pixels, width_in_meters, height_in_meters)

# 2. Calculate distances from a list of player positions per frame:
distances = calculator.calculate_distance(tactical_player_positions)

# 3. Calculate speeds (km/h) from distances:
speeds = calculator.calculate_speed(distances, fps=30)


