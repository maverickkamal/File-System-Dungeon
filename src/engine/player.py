from dataclasses import dataclass, field

@dataclass
class Player:

    hp: int = 100
    max_hp: int = 100
    level: int = 1
    xp: int = 0
    xp_to_next_level: int = 100
    inventory: list = field(default_factory=list)

    def take_damage(self, amount: int) -> int:

        self.hp = max(0, self.hp - amount)
        return amount
    
    def heal(self, amount: int) -> int:
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp
    def gain_xp(self, amount: int) -> bool:
        self.xp += amount
        leveled_up = False
        while self.xp >= self.xp_to_next_level:
            self._level_up()
            leveled_up = True
        return leveled_up
    def _level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        self.max_hp += 10
        self.hp = self.max_hp

    def add_item(self, item: dict) -> None:
        self.inventory.append(item)

    def to_dict(self) -> dict:
        return {
            "hp": self.hp,
            "max_hp": self.max_hp,
            "level": self.level,
            "xp": self.xp,
            "xp_to_next_level": self.xp_to_next_level,
            "inventory": self.inventory
        }
    def from_dict(self, data: dict) -> None:
        self.hp = data.get("hp", 100)
        self.max_hp = data.get("max_hp", 100)
        self.level = data.get("level", 1)
        self.xp = data.get("xp", 0)
        self.xp_to_next_level = data.get("xp_to_next_level", 100)
        self.inventory = data.get("inventory", [])
