import cv2
class TacticalView:
  def __init__(self,court_image_path):
    self.court_image_path=court_image_path
    self.width=300
    self.height= 161
    self.actual_width_in_meters=28
    self.actual_height_in_meters=15
    self.keypoints= [
      # left edge
      (0,0),
      (0,int((0.91/self.actual_height_in_meters)*self.height)),
      (0,int((5.18/self.actual_height_in_meters)*self.height)),
      (0,int((10/self.actual_height_in_meters)*self.height)),
      (0,int((14.1/self.actual_height_in_meters)*self.height)),
      (0,int(self.height)),

      # Middle line
      (int(self.width/2),self.height),
      (int(self.width/2),0),

      # Left Free throw line
      (int((5.79/self.actual_width_in_meters)*self.width),int((5.18/self.actual_height_in_meters)*self.height)),
      (int((5.79/self.actual_width_in_meters)*self.width),int((10/self.actual_height_in_meters)*self.height)),

    ]    
    
