"""
After experimenting with many yolos versions, the best for the ball detection was yolov5 with 250 epochs
"""

# Libraries and setup
from roboflow import Roboflow
from ultralytics import YOLO


# Get the dataset that is compatible with the yolov5 model
rf = Roboflow(api_key="Your_API_Key") #Replace with your API Key
project = rf.workspace("workspace-5ujvu").project("basketball-players-fy4c2-vfsuv")
version = project.version(17)
dataset = version.download("yolov5")

# Train YOLOv5
model_path = 'yolov5l6u.pt'
data_yaml_path = f'{dataset.location}/data.yaml' 
imgsz = 640
epochs = 250
batch = 8

# Load model
model = YOLO(model_path)

# Train the model
model.train(data=data_yaml_path, epochs=epochs, imgsz=imgsz, batch=batch, plots=True)
