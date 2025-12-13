import random
import math
from src.engine.player import Player

class CombatEngine:

    @staticmethod
    def calculate_player_damage(player: Player) -> int:
        base_damage = 5
        variation = random.uniform(0.8, 1.2)
        damage = int((base_damage + (player.level * 2)) * variation)
        return max(1, damage)
    
    @staticmethod
    def calculate_enemy_damage(enemy_entity: dict) -> int:

        size = enemy_entity.get("size_bytes", 0)
        if size == 0:
            return 1
        base_dmg = math.log10(size)

        etype = enemy_entity.get("type", "Minions")
        multiplier = 1.0
        if etype == "Boss":
            multiplier = 2.0
        elif etype == "Construct":
            multiplier = 0.8

        damage = int(base_dmg * multiplier * random.uniform(0.8, 1.2))
        return max(1, damage)
    
    @staticmethod
    def resolve_turn(player: Player, enemy_entity: dict) -> list[str]:

        logs = []

        p_dmg = CombatEngine.calculate_player_damage(player)

        enemy_entity["hp"] -= p_dmg
        logs.append(f"You hit {enemy_entity["name"]} for {p_dmg} damage!")

        if enemy_entity["hp"] <= 0:
            enemy_entity["hp"] = 0
            logs.append(f"{enemy_entity["name"]} was defeated!")
            player.gain_xp(10)
            logs.append("You gained 10 XP!!")
            return logs
        
        e_dmg = CombatEngine.calculate_enemy_damage(enemy_entity)
        player.take_damage(e_dmg)
        logs.append(f"{enemy_entity["name"]} hits you for {e_dmg} damage!")

        if player.hp <= 0:
            logs.append("You have been defeated.... Game Over.")
        return logs