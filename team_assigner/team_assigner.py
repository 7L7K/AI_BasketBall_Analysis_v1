import cv2
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from typing import List, Dict, Tuple
import sys
sys.path.append("..")  # Adjust path if needed

from utils import read_stub, save_stub

class TeamAssigner:
    def __init__(self, team1_class_name = "white shirt", team2_class_name = "dark blue shirt"):
        """
        Initialize the TeamAssigner with team class names (as described to Fashion-CLIP).
        """
        self.team1_class_name = team1_class_name
        self.team2_class_name = team2_class_name
        self.player_team_dict = {}
        self.model = None
        self.processor = None

    def load_model(self):
        """
        Load the Fashion-CLIP model and processor from Hugging Face.
        """
        self.model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
        self.processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")

    def get_player_color(self, frame, bbox) :
        """
        Predict the jersey color of a player by classifying cropped region using Fashion-CLIP.
        """
        x1, y1, x2, y2 = bbox
        image = frame[int(y1):int(y2), int(x1):int(x2)]

        if image.size == 0:
            return "unknown"

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)

        classes = [self.team1_class_name, self.team2_class_name]
        inputs = self.processor(text=classes, images=pil_image, return_tensors="pt", padding=True)

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1)

        return classes[probs.argmax(dim=1).item()]

    def get_player_team(self, frame, player_bbox, player_id):
        """
        Assign a team ID to a player based on jersey color.
        """
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id]

        player_color = self.get_player_color(frame, player_bbox)
        team_id = 1 if player_color == self.team1_class_name else 2

        self.player_team_dict[player_id] = team_id
        return team_id

    def get_player_team_across_frames(
        self,
        video_frames,
        player_tracks,
        read_from_stub = False,
        stub_path = None
    ):
        """
        Assign teams to all players across all frames.
        Caches results to a stub file if needed.
        """
        cached = read_stub(read_from_stub, stub_path)
        if cached is not None and len(cached) == len(video_frames):
            return cached

        self.load_model()
        player_assignments = []

        for frame_num, frame_tracks in enumerate(player_tracks):
            current_frame_assignment = {}

            if frame_num % 50 == 0:
                self.player_team_dict = {}  # Reset dict periodically

            for player_id, track_data in frame_tracks.items():
                bbox = track_data["bbox"]
                team = self.get_player_team(video_frames[frame_num], bbox, player_id)
                current_frame_assignment[player_id] = team

            player_assignments.append(current_frame_assignment)

        save_stub(stub_path, player_assignments)
        return player_assignments
