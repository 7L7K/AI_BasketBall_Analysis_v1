# Libraries and setup
from roboflow import Roboflow
import shutil
from ultralytics import YOLO


# Get the dataset that is compatible with the yolov5 model
rf = Roboflow(api_key="9yPpcn0aDPnKVNT67zUg")
project = rf.workspace("workspace-5ujvu").project("basketball-players-fy4c2-vfsuv")
version = project.version(17)
dataset = version.download("yolov5")

# Moving the train and valid dataset: this is necessary for the yolov5 model
shutil.move("Basketball-Players-17/train", "Basketball-Players-17/Basketball-Players-17/train")
shutil.move("Basketball-Players-17/valid", "Basketball-Players-17/Basketball-Players-17/valid")

# Train YOLOv5
model_path = 'yolov5l6u.pt'
data_yaml_path = f'{dataset.location}/data.yaml' 
imgsz = 640
epochs = 100
batch = 8

# Load model
model = YOLO(model_path)

# Train the model
model.train(data=data_yaml_path, epochs=epochs, imgsz=imgsz, batch=batch, plots=True)
