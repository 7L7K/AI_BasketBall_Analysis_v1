import shutil 

# Moving the train and valid dataset: this is necessary for the yolov5 model
shutil.move("Basketball-Players-17/train", "Basketball-Players-17/Basketball-Players-17/train")
shutil.move("Basketball-Players-17/valid", "Basketball-Players-17/Basketball-Players-17/valid")
