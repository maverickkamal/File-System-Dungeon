import json
from pathlib import Path
from datetime import datetime
from src.engine.player import Player

class SaveManager:

    SAVE_FILE = Path("save_state.json")

    def __init__(self):
        self.dungeon_data = {}

    def load_game(self, player: Player) -> None:
        if not self.SAVE_FILE.exists():
            return
        
        try:
            with open(self.SAVE_FILE, "r") as f:
                data = json.load(f)
            
            player_data = data.get("player", {})
            if player_data:
                player.from_dict(player_data)

            self.dungeon_data = data.get("dungeon", {})
        except Exception as e:
            print(f"Error loading save: {e}")
    
    def save_game(self, player: Player) -> None:
        data = {
            "player": player.to_dict(),
            "dungeon": self.dungeon_data
        }

        try:
            with open(self.SAVE_FILE, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving game: {e}")
    
    def mark_defeated(self, file_path: str) -> None:
        self.dungeon_data[file_path] = {
            "status": "defeated",
            "timestamp": datetime.now().isoformat()
        }
    
    def is_defeated(self, file_path: str) -> bool:
        return file_path in self.dungeon_data