"""
team_assigner.py

Assigns teams to players across video frames using Fashion-CLIP model.
Determines team ID based on jersey color classification.
"""

import sys
from typing import List, Dict, Tuple, Optional

import cv2
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# Add parent directory to path if needed
sys.path.append("..")

from utils import read_stub, save_stub


class TeamAssigner:
    """
    Assigns team IDs to tracked players based on jersey color using the Fashion-CLIP model.
    """

    def __init__(
        self,
        team1_class_name: str = "white shirt",
        team2_class_name: str = "dark blue shirt"
    ):
        """
        Initialize the TeamAssigner with class names for team uniforms.
        """
        self.team1_class_name = team1_class_name
        self.team2_class_name = team2_class_name
        self.player_team_dict: Dict[int, int] = {}
        self.model: Optional[CLIPModel] = None
        self.processor: Optional[CLIPProcessor] = None

    def load_model(self) -> None:
        """
        Load the pre-trained Fashion-CLIP model and processor from Hugging Face.
        """
        self.model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
        self.processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")

    def get_player_color(self, frame, bbox: Tuple[int, int, int, int]) -> str:
        """
        Predict the jersey color by classifying a cropped player image.
        """
        x1, y1, x2, y2 = bbox
        image = frame[int(y1):int(y2), int(x1):int(x2)]

        if image.size == 0:
            return "unknown"

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)

        class_names = [self.team1_class_name, self.team2_class_name]
        inputs = self.processor(
            text=class_names,
            images=pil_image,
            return_tensors="pt",
            padding=True
        )

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1)

        return class_names[probs.argmax(dim=1).item()]

    def get_player_team(self, frame, bbox: Tuple[int, int, int, int], player_id: int) -> int:
        """
        Assign a team ID to a player based on jersey classification.
        """
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id]

        color_class = self.get_player_color(frame, bbox)
        team_id = 1 if color_class == self.team1_class_name else 2
        self.player_team_dict[player_id] = team_id

        return team_id

    def get_player_team_across_frames(
        self,
        video_frames: List,
        player_tracks: List[Dict[int, Dict[str, Tuple[int, int, int, int]]]],
        read_from_stub: bool = False,
        stub_path: Optional[str] = None
    ) -> List[Dict[int, int]]:
        """
        Assign teams to players across all frames using jersey color detection.
        """
        cached = read_stub(read_from_stub, stub_path)
        if cached is not None and len(cached) == len(video_frames):
            return cached

        self.load_model()
        player_assignments = []

        for frame_num, frame_tracks in enumerate(player_tracks):
            current_assignment: Dict[int, int] = {}

            # Reset tracking dictionary periodically
            if frame_num % 50 == 0:
                self.player_team_dict = {}

            for player_id, track_data in frame_tracks.items():
                bbox = track_data.get("bbox")
                if bbox:
                    team_id = self.get_player_team(video_frames[frame_num], bbox, player_id)
                    current_assignment[player_id] = team_id

            player_assignments.append(current_assignment)

        save_stub(stub_path, player_assignments)
        return player_assignments
