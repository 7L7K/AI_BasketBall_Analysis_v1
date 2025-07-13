"""
dataset_config.py

Moves the train/valid directories inside the expected YOLOv5 format directory.

Example:
If dataset is downloaded to "Basketball-Players-17/", this script moves:
- Basketball-Players-17/train → Basketball-Players-17/Basketball-Players-17/train
- Basketball-Players-17/valid → Basketball-Players-17/Basketball-Players-17/valid
"""

import os
import shutil


def move_yolo_subdirs(dataset_path):
    """
    Move 'train' and 'valid' folders into the expected YOLOv5 structure:
    dataset_path/train -> dataset_path/dataset_name/train

    Args:
        dataset_path (str): Root path to the downloaded dataset folder.
    """
    dataset_name = os.path.basename(dataset_path)
    target_dir = os.path.join(dataset_path, dataset_name)

    os.makedirs(target_dir, exist_ok=True)

    for split in ['train', 'valid']:
        src = os.path.join(dataset_path, split)
        dst = os.path.join(target_dir, split)

        if os.path.exists(src):
            print(f"[INFO] Moving '{split}' from {src} → {dst}")
            shutil.move(src, dst)
        else:
            print(f"[WARNING] '{split}' folder not found in {dataset_path}")


if __name__ == "__main__":
    # Our dataset from Roboflow
    dataset_root = "Basketball-Players-17"
    move_yolo_subdirs(dataset_root)
