from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DirectoryTree, DataTable, Label
from textual.reactive import reactive
from pathlib import Path
from typing import Optional
from src.ui.widgets import Sidebar, RoomView
from src.engine.scanner import Scanner
from src.ui.screen import CombatModal
from src.engine.player import Player
from src.engine.persistence import SaveManager
from src.engine.combat import CombatEngine
from src.ui.screen import InventoryModal

class FileSystemDungeonApp(App):
    """ A TUI RPG exploring the file system as dungeons. """

    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
        grid-columns: 1fr 3fr;
    }
    .box {
        height: auto;
        border: solid green;
        margin: 1;
        padding: 1;
    }
    .label {
        background: $primary;
        color: $text;
        padding: 0 1;
        width: 100%;
        text-align: center;
    }
    #radar {
        height: 1fr;
        border: solid blue;
    }
    #room_table {
        height: 100%;
        border: solid red;
    }
    """

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
        ("i", "open_inventory", "Inventory")
    ]

    current_path = reactive(Path.home())
    current_entities = {}
    player = Player()
    save_manager = SaveManager()
    active_combat_entity = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Sidebar()
        yield RoomView()
        yield Footer()

    def on_mount(self) -> None:
        self.save_manager.load_game(self.player)
        self.scan_current_room()
        self.update_sidebar_stats()

    def update_sidebar_stats(self) -> None:
        try:
            self.query_one("#stats-title", Label).update(f"Player Level: {self.player.level}\nXP: {self.player.xp}")

        except:
            pass

    def on_directory_tree_directory_selected(self, event: DirectoryTree.DirectorySelected) -> None:

        self.current_path = Path(event.path)
        self.scan_current_room()
    
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        row_index = event.cursor_row
        if row_index < 0 or row_index >= len(self.current_entities):
            return
        entity = self.current_entities.get(row_index)
        if not entity:
            return
        
        if entity.get('is_dir'):
            return
        
        if entity.get('type') == 'Looted':
            self.notify("Already looted.")
            return
        
        self.active_combat_entity = entity
        self.push_screen(CombatModal(entity, self.player), self.handle_combat_result)

    def handle_combat_result(self, result: Optional[str]) -> None:
        self.update_sidebar_stats()

        if result == "run":
            self.notify("You fled safely!")
        elif result == "victory":
            self.notify("Victory! You looted the foe")

            if self.active_combat_entity:
                xp_gain = CombatEngine.calculate_xp_reward(self.active_combat_entity)
                if self.player.gain_xp(xp_gain):
                    self.notify(f"LEVEL UP! You are now level {self.player.level}!", severity="warning")
                else:
                    self.notify(f"Gained {xp_gain} XP!")

                loot_item = self.active_combat_entity.copy()
                loot_item['name'] = f"Essence of {loot_item['name']}"
                self.player.add_item(loot_item)
                self.notify(f"Picked up: {loot_item['name']}")

                self.save_manager.mark_defeated(self.active_combat_entity['path'])
                self.save_manager.save_game(self.player)
                self.scan_current_room()

        elif result == "defeat":
            self.notify("You died... Respawning...", severity="error")
            self.player.hp = self.player.max_hp
            self.save_manager.save_game(self.player)
            self.update_sidebar_stats()
    
    def action_open_inventory(self) -> None:
        self.push_screen(InventoryModal(self.player.inventory))

    def scan_current_room(self) -> None:
        
        current_path_str = str(self.current_path)
        if not self.save_manager.is_visited(current_path_str):
            self.save_manager.mark_visited(current_path_str)

            if self.player.gain_xp(10):
                self.notify(f"LEVEL UP! You are now level {self.player.level}!")
            else:
                self.notify("New Room Discoveres! +10 XP")
            self.save_manager.save_game(self.player)
            self.update_sidebar_stats()

        result = Scanner.scan_room(self.current_path, self.save_manager)
        table = self.query_one(DataTable)
        table.clear()
        self.current_entities = {}

        row_count = 0

        if result.access_denied:
            table.add_row("LOCKED GATE", "Access Denied", "---", "---")
            return
        for entity in result.entities:
            table.add_row(
                entity["name"],
                entity["type"],
                str(entity["hp"]),
                str(entity["size_bytes"])
            )
            self.current_entities[row_count] = entity
            row_count += 1
        self.sub_title = str(self.current_path)
    
    def action_toggle_dark(self) -> None:
        self.theme = "textual-light" if self.theme == "textual-dark" else "textual-dark"