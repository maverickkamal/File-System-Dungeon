from dataclasses import dataclass

@dataclass
class Player:

    hp: int = 100
    max_hp: int = 100
    level: int = 1
    xp: int = 0
    xp_to_next_level: int = 100

    def take_damage(self, amount: int) -> int:

        actual_damage = min(self.hp, amount)
        self.hp -= actual_damage
        return actual_damage
    def heal(self, amount: int) -> int:
        missing_hp = self.max_hp =- self.hp
        actual_heal = min(missing_hp, amount)
        self.hp += actual_heal
        return actual_heal
    def gain_xp(self, amount: int) -> bool:
        self.xp += amount
        if self.xp >= self.xp_to_next_level:
            self._level_up()
            return True
        return False
    def _level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        self.max_hp += 10
        self.hp = self.max_hp
