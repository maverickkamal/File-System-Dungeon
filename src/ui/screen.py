from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, Button, Static, RichLog, DataTable
from textual.containers import Grid, Horizontal, Vertical, Container
from src.engine.player import Player
from src.engine.combat import CombatEngine

class CombatModal(ModalScreen):

    CSS = """
    CombatModal {
        align: center middle;
    }

    #dialog {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1fr 3fr 1fr;
        padding: 0 1;
        width: 70;
        height: 20;
        border: thick $background 80%;
        background: $surface;
    }

    #question {
        column-span: 2;
        height: 1fr;
        width: 1fr;
        content-align: center middle;
        text-align: center;
        background: $primary-darken-2;
    }

    #stats_container {
        column-span: 2;
        height: 1fr;
        layout: horizontal;
    }

    .stat-box {
        width: 1fr;
        border: solid $accent;
        padding: 1;
    }

    #log {
        column-span: 2;
        height: 1fr;
        border: solid $secondary;
        overflow-y: scroll;
    }

    #buttons {
        column-span: 2;
        height: auto;
        width: 1fr;
        align: center bottom;
        margin-top: 1;
    }

    Button {
        width: 3%;
        margin: 0 1;
    }
    """

    def __init__(self, entity_data: dict, player: Player):
        super().__init__()
        self.entity_data = entity_data
        self.player = player

    def compose(self) -> ComposeResult:
        with Grid(id="dialog"):
            yield Label(f"ENCOUNTER: {self.entity_data['name']}", id="question")

            with Container(id="stats_container"):
                yield Label(self._get_enemy_stats_text(), id="enemy_stats", classes="stat-box")
                yield Label(self._get_player_stats_text(), id="player_stats", classes="stat-box")

            yield RichLog(id="log", highlight=True, markup=True)

            with Horizontal(id="buttons"):
                yield Button("Attack", variant="error", id="btn_attack")
                yield Button("Inspect", variant="primary", id="btn_inspect")
                yield Button("Run", variant="default", id="btn_run")
    def _get_enemy_stats_text(self) -> str:
        return (
            f"[bold red]ENEMY[/]\n"
            f"Type: {self.entity_data['type']}\n"
            f"HP: {self.entity_data['hp']} / {self.entity_data['max_hp']}\n"
        )
    
    def _get_player_stats_text(self) -> str:
        return (
            f"[bold green]PLAYER[/]\n"
            f"Lv1: {self.player.level}\n"
            f"HP: {self.player.hp} / {self.player.max_hp}"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        log = self.query_one(RichLog)

        if event.button.id == "btn_run":
            self.dismiss("run")
        elif event.button.id == "btn_inspect":
            log.write(f"Size: {self.entity_data['size_bytes']} bytes")
            log.write(f"Path: {self.entity_data['path']}")
        elif event.button.id == "btn_attack":
            self._handle_attack(log)
        elif event.button.id == "btn_leave":
            self.dismiss()

    def _handle_attack(self, log: RichLog) -> None:
        logs = CombatEngine.resolve_turn(self.player, self.entity_data)
        for msg in logs:
            log.write(msg)
        
        self.query_one("#enemy_stats", Label).update(self._get_enemy_stats_text())
        self.query_one("#player_stats", Label).update(self._get_player_stats_text())

        if self.entity_data['hp'] <= 0:
            log.write("[bold gold]VICTORY![/]")
            self.query_one("#buttons").remove()
            self.mount(Button("Loot & Leave", variant="success", id="btn_leave"))

        if self.player.hp <= 0:
            log.write("[bold red]DEFEATED![/]")
            self.dismiss("defeat")

class InventoryModal(ModalScreen):

    CSS = """"
    InventoryModal {
        align: center middle;
    }
    #inventory-dialog {
        grid-size: 1;
        grid-gutter: 1;
        grid-rows: 1fr 3;
        padding: 0 1;
        width: 60;
        height: 80%;
        border: thick $background 80%;
        background: $surface;
    }
    #inventory-table {
        height: 1fr;
    }
    """

    def __init__(self, inventory: list):
        self.inventory = inventory
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Inventory", id="title"),
            DataTable(id="inventory-table"),
            Button("Close", variant="primary", id="close"),
            id="inventory-dialog",
        )

    def on_mount(self) -> None:
        table = self.query_one("#inventory-table", DataTable)
        table.cursor_type = 'row'
        table.add_columns("Name", "Type", "Size")

        for item in self.inventory:
            table.add_row(item.get("name", "Unknown"), item.get("type", "?"), str(item.get("size_bytes", 0)))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close":
            self.dismiss()
