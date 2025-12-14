from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional
from .stats import StatFactory

@dataclass
class ScanResult:
    """Will represents the result of a directory scan."""
    path: Path
    entities: List[dict] = field(default_factory=list)
    access_denied: bool = False
    error_message: Optional[str] = None

class Scanner:
    """Will handle file system scanning and entity generation."""

    @staticmethod
    def scan_room(path: Path, save_manager=None) -> ScanResult:
        """
        Scans a directory (Room) and returns a list of entities (Files/Monsters).
        Also checks save_manager for defeated status if provided
        """

        entities = []
        access_denied = False
        error_msg = None

        if not path.exists():
            return ScanResult(path, error_message="Path does not exist.")
        
        try: 
            for item in path.iterdir():
                if item.name.startswith("."):
                    continue
            
                stats = StatFactory.get_stats(item)

                if item.is_dir():
                    stats["type"] = "Portal"
                    stats["hp"] = "N/A"
                else:
                    if save_manager and save_manager.is_defeated(str(item)):
                        stats["hp"] = 0
                        stats["type"] = "Looted"
                        stats["name"] = f"[x] {stats['name']}"

                entities.append(stats)
        except PermissionError:
            access_denied = True
            error_msg = "LOCKED GATE: Permission Denied"
        except Exception as e:
            error_msg = f"Unknown Error: {str(e)}"
        return ScanResult(
            path=path,
            entities=entities,
            access_denied=access_denied,
            error_message=error_msg
        )