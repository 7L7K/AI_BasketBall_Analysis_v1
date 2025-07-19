import os
from roboflow import Roboflow
import subprocess

def download_dataset(api_key: str, workspace: str, project_name: str, version_number: int, format: str = "yolov8") -> str:
    """
    Downloads a Roboflow dataset and returns the local path to the dataset directory.
    """
    rf = Roboflow(api_key=api_key)
    project = rf.workspace(workspace).project(project_name)
    version = project.version(version_number)
    dataset = version.download(format)
    return dataset.location

def train_pose_model(data_yaml_path: str,
                     model: str = "yolov8x-pose.pt",
                     imgsz: int = 640,
                     batch: int = 16,
                     epochs: int = 500,
                     plots: bool = True):
    """
    Runs the training command for a YOLOv8 pose model using the Ultralytics CLI.
    """
    cmd = [
        "yolo",
        "task=pose",
        "mode=train",
        f"model={model}",
        f"data={data_yaml_path}",
        f"imgsz={imgsz}",
        f"batch={batch}",
        f"epochs={epochs}",
        f"plots={str(plots).lower()}"
    ]

    print("Running training command:")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    # Set up parameters
    API_KEY = "Your_API_Key_here"
    WORKSPACE = "fyp-3bwmg"
    PROJECT_NAME = "reloc2-den7l"
    VERSION = 1

    # Download dataset
    print("Downloading dataset from Roboflow...")
    dataset_path = download_dataset(api_key=API_KEY,
                                     workspace=WORKSPACE,
                                     project_name=PROJECT_NAME,
                                     version_number=VERSION)

    # Compose full path to data.yaml
    data_yaml_path = os.path.join(dataset_path, "data.yaml")

    # Train the model
    train_pose_model(data_yaml_path=data_yaml_path)
