from PIL import Image
from transformers import CLIPProcessor, CLIPModel

class TeamAssigner:
  def __init__(self, team1_class_name="white shirt", team2_class_name="dark blue shirt"):
    self.team1_class_name=team1_class_name
    self.team2_class_name=team2_class_name

def load_model(self):
  self.model=CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
  self.processor=CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")

def get_player_color(self,frame,bbox):
  # Cropping the image of the player in the frame
  x1,y1,x2,y2=bbox
  image=frame[int(y1):int(y2), int(x1):int(x2)]

  rgb_image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
  pil_image=Image.fromarray(rgb_image)

  classes=[self.team1_class_name, self.team2_class_name]
  inputs= self.processor(text=classes, images=pil_image, return_tensors="pt", padding=True)

  outputs =self.model(**inputs)
  logits_per_image = outputs.logits_per_image
  probs = logits_per_image.softmax(dim=1)

  return classes[probs.argmax(dim=1)[0]] #Index with the highest probability
