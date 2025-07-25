from .utils import draw_traingle

class BallTracksDrawer:
    def __init__(self):
        """
        Initialize the BallTracksDrawer instance with custom colors.
        """
        self.ball_color_in_possession = (0, 140, 255)  # Orange
        self.ball_color_free = (255, 0, 255)           # Magenta

    def draw(self, video_frames, tracks, ball_aquisition):
        """
        Draws ball pointers on each video frame based on tracking and possession info.
        """
        output_video_frames = []
        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()
            ball_dict = tracks[frame_num]

            for _, ball in ball_dict.items():
                if ball["bbox"] is None:
                    continue

                if ball_aquisition[frame_num] is not None:
                    color = self.ball_color_in_possession
                else:
                    color = self.ball_color_free

                frame = draw_traingle(frame, ball["bbox"], color)

            output_video_frames.append(frame)
        return output_video_frames
