import cv2

class TacticalViewDrawer:
    """
    Overlays a tactical basketball court view on a sequence of video frames.
    This is useful for spatially contextualizing player and ball positions.
    """

    def __init__(self, start_x: int = 20, start_y: int = 40):
        """
        Initializes the tactical drawer with offset coordinates.
        """
        self.start_x = start_x
        self.start_y = start_y

    def draw(self, video_frames, court_image_path: str, width: int, height: int, tactical_court_keypoints):
        """
        Draws a semi-transparent court image overlay on each video frame.
        """
        court_image = cv2.imread(court_image_path)
        court_image = cv2.resize(court_image, (width, height))

        output_video_frames = []
        for frame in video_frames:
            frame = frame.copy()
            y1, x1 = self.start_y, self.start_x
            y2, x2 = y1 + height, x1 + width

            # Ensure the overlay fits within the frame
            if y2 > frame.shape[0] or x2 > frame.shape[1]:
                raise ValueError("Court image exceeds frame boundaries. Adjust start_x/start_y or image size.")

            overlay = frame[y1:y2, x1:x2].copy()
            blended = cv2.addWeighted(court_image, 0.6, overlay, 0.4, 0)
            frame[y1:y2, x1:x2] = blended

            for keypoint_index, keypoint in enumerate(tactical_court_keypoints):
                x,y=keypoint
                x+=self.start_x
                y+=self.start_y
                cv2.circle(frame, (x,y), 5 , (0,0,255),-1)
                cv2.putText(frame, str(key_point_index), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0),2)
                

            output_video_frames.append(frame)

        return output_video_frames
