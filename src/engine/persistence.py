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
    
    def quarantine_file(self, file_path: str) -> bool:
        """
        Try making a logic that moves file to a quarantine folder.
        """
        try:
            target = Path(file_path)
            if not target.exists():
                return False
            quarantine_dir = self.SAVE_FILE.parent / "quarantines"
            quarantine_dir.mkdir(exist_ok=True)

            safe_name = f"{target.name} {int(datetime.now().timestamp())}"
            dest = quarantine_dir / safe_name

            target.rename(dest)

            self.dungeon_data[str(target)]["quarantine_path"] = str(dest) 
            return True
        except Exception as e:
            print(f"Quarantine failed: {e}")
            return False
    
    def is_defeated(self, file_path: str) -> bool:
        return file_path in self.dungeon_data
    
    def mark_visited(self, path: str) -> None:
        if path not in self.dungeon_data:
            self.dungeon_data[path] = {}

        self.dungeon_data[path]["visited"] = True
        self.dungeon_data[path]["last_visited"] = datetime.now().isoformat()
    
    def is_visited(self, path: str) -> bool:
        data = self.dungeon_data.get(path, {})
        return data.get("visited", False)