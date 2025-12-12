from pathlib import Path
import math

class StatFactory:
    """Handles game statistics for file entities"""

    TYPE_MAPPING = {
        "Construct": {".py", ".js", ".c", ".rs", ".java", ".go", ".cpp", ".ts"},
        "Illusion": {".png", ".jpg", ".jpeg", ".gif", ".mp4", ".mov", ".avi", ".mkv", ".svg"},
        "Archive": {".zip", ".tar", ".gz", ".rar", ".7z", ".bzz"},
        "Boss": {".exe", ".dll", ".bin", ".sys", ".bat", ".sh", ".msi", ".app"},
        "Lore": {".txt", ".md", ".json", ".log", ".xml", ".yml", ".yaml"}
    }

    HP_PER_KB = 1
    MAX_BOSS_HP = 9999
    BOSS_SIZE_THRESHOLD = 500 * 1024 * 1024 

    @classmethod
    def get_stats(cls, file_path: Path) -> dict:
        """
        Generates a stats dictionary for a given file path.
        """
        try:
            stat_info = file_path.stat()
            size = stat_info.st_size
        except (FileNotFoundError, PermissionError):
            size = 0

        return {
            "name": file_path.name,
            "path": str(file_path),
            "hp": cls._calculate_hp(size),
            "max_hp": cls._calculate_hp(size),
            "type": cls._determine_type(file_path.suffix),
            "size_bytes": size,
            "is_dir": file_path.is_dir()

        }
    
    @classmethod
    def _calculate_hp(cls, size_bytes: int) -> int:
        if size_bytes >= cls.BOSS_SIZE_THRESHOLD:
            return cls.MAX_BOSS_HP
        hp = math.ceil(size_bytes / 1024)
        return max(1, hp)
    
    @classmethod
    def _determine_type(cls, suffix: str) -> str:
        suffix = suffix.lower()

        for entity_type, extensions in cls.TYPE_MAPPING.items():
            if suffix in extensions:
                return entity_type
            
        return "Minion"