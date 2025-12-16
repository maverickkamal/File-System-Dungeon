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
        grid-rows: auto auto 1fr auto;
        padding: 0 1;
        width: 70;
        height: 25;
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
        width: auto;
        min-width: 0;
        padding: 0 1;
        margin: 0 1;
    }
    """

    def __init__(self, entity_data: dict, player: Player):
        super().__init__()
        self.entity_data = entity_data
        self.player = player

    BINDINGS = [
        ("b", "run_away", "Run Away"),
        ("escape", "run_away", "Run Away"),
    ]

    def action_run_away(self) -> None:
        self.dismiss("run")

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
                if self.entity_data.get("type") == "Lore": 
                    yield Button("Read", variant="warning", id="btn_read")
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
            f"Lvl: {self.player.level}\n"
            f"HP: {self.player.hp} / {self.player.max_hp}"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        log = self.query_one(RichLog)

        if event.button.id == "btn_run":
            self.dismiss("run")
        elif event.button.id == "btn_inspect":
            blocks = self.entity_data.get('size_bytes', 0)
            msg = f"Path: {self.entity_data['path']}\nSize; {blocks} bytes"
            log.write(f"[bold cyan]INSPECT:[/] {msg}")
            self.app.notify(f"Inspect: {blocks} bytes", title=self.entity_data['name'])
        elif event.button.id == "btn_read":
            self.dismiss("read")
        elif event.button.id == "btn_attack":
            self._handle_attack(log)
        elif event.button.id == "btn_leave":
            self.dismiss("victory")
    def _handle_attack(self, log: RichLog) -> None:
        logs = CombatEngine.resolve_turn(self.player, self.entity_data)
        for msg in logs:
            log.write(msg)

        self.query_one("#enemy_stats", Label).update(self._get_enemy_stats_text())
        self.query_one("#player_stats", Label).update(self._get_player_stats_text())

        if self.entity_data['hp'] <= 0:
            log.write("[bold gold1]VICTORY![/]")
            self.query_one("#buttons").remove()
            self.mount(Button("Loot & Leave", variant="success", id="btn_leave"))

        if self.player.hp <= 0:
            log.write("[bold red]DEFEATED![/]")
            self.dismiss("defeat")

class InventoryModal(ModalScreen):

    CSS = """
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
        table.cursor_type = "row"
        table.add_columns("Name", "Type", "Size")

        for item in self.inventory:
            table.add_row(item.get("name", "Unknown"), item.get("type", "?" ), str(item.get("size_bytes", 0)))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close":
            self.dismiss()

class LoreModal(ModalScreen):

    CSS = """
    LoreModal {
        width: 80;
        height: 80%;
        border: thick gold;
        background: $surface;
        padding: 1;
    }
    #lore-content {
        height: 1fr;
        border: solid $secondary;
        overflow-y: scroll;
        margin-bottom: 1;
    }
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(f"Reading: {self.file_path}", id="title"),
            RichLog(id="lore-content", highlight=True, markup=False),
            Button("Close", variant="primary", id="close"),
            id="lore-dialog",
        )

    def on_mount(self) -> None:
        log = self.query_one(RichLog)
        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(2000)
                if len(content) == 0:
                    log.write("The file is empty.")
                else:
                    log.write(content)
                if len(content) == 2000:
                    log.write("\n... [Truncated] ...")
        except Exception as e:
            log.write(f"Failed to read ancient runes: {e}")
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss()