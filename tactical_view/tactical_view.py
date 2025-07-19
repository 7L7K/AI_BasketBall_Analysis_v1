import cv2
class TacticalView:
  def __init__(self,court_image_path):
    self.court_image_path=court_image_path
    self.width=300
    self.height= 161
    self.actual_width=28
    self.actual_height=15
    

  def mapping(self, court_keypoints):
    
    
