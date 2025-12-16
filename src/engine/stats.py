from pathlib import Path
import math

class StatFactory:
    """Handles game statistics for file entities"""

    TYPE_MAPPING = {
        "Construct": {".py", ".js", "jsx", ".ts", ".html", ".css", ".scss" ".c", ".rs", ".java", ".go", ".cpp", ".ts"},
        "Illusion": {".png", ".jpg", ".jpeg", ".gif", ".mp4", ".mov", ".avi", ".mkv", ".svg", ".bmp", ".ico", ".mp3", ".wav", ".ogg"},
        "Archive": {".zip", ".tar", ".gz", ".rar", ".7z", ".bzz", ".iso"},
        "Boss": {".exe", ".dll", ".bin", ".sys", ".bat", ".sh", ".msi", ".app", ".info", ".cmd"},
        "Lore": {".txt", ".md", ".json", ".log", ".xml", ".yml", ".yaml", ".ini", ".cfg", ".csv", ".toml", ".env"}
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

        entity_type = cls._determine_type(file_path.suffix)

        return {
            "name": file_path.name,
            "path": str(file_path),
            "hp": cls._calculate_hp(size),
            "max_hp": cls._calculate_hp(size),
            "type": entity_type,
            "color": cls._get_color(entity_type),
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
    
    @staticmethod
    def _get_color(entity_type: str) -> str:
        mapping = {
            "Boss": "bold red",
            "Construct": "bold blue",
            "Iluusion": "bold magenta",
            "Lore": "bold yellow",
            "Archive": "bold gold",
            "Portal": "bold cyan",
            "Minion": "white"
        }
        return mapping.get(entity_type, "white")