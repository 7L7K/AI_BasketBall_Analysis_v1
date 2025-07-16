from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import sys
sys.path.append("/../")
from utils import read_stub, save_stub

class TeamAssigner:
  def __init__(self, team1_class_name="white shirt", team2_class_name="dark blue shirt"):
    self.team1_class_name=team1_class_name
    self.team2_class_name=team2_class_name
    self.player_team_dict={}

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



  def get_player_team(self, frame, player_bbox, player_id):
    if player_id in self.player_team_dict:
      return self.player_team_dict[player_id]
    else:
      player_color=self.get_player_color(frame, player_bbox)
      team_id=2
      if player_color==self.team1_class_name:
        team_id=1
  
      self.team_player_dict[player_id]=team_id
      return team_id


  def get_player_team_across_frame(self, video_frames, player_tracks, read_from_stub=False,stub_path=None):
    player_assignment=read_stub(read_from_stub, stub_path)
    if player_assignment in not None:
      if len(player_assignment)==len(video_frames):
        return player_assignment
    self.load_model()
    player_assignment=[]
    for frame_num, player_track in enumerate(player_tracks):
      player_assignment.append({})
      if frame_num % 50 ==0:
        self.player_tean_dict={}
      for player_id, track in player_tracks.items():
        team=self.get_player_team(vide_frames[frame_num], track["bbox"], player_id)
        player_assignment[frame_num][player_id]=team
        
  save_stub(stub_path, player_assignment)
  return player_assignment 


        
        


    
    
  
