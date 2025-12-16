from textual.app import ComposeResult
from textual.widgets import DirectoryTree, Static, DataTable, Label
from textual.containers import Vertical, Container
from pathlib import Path

class PlayerStats(Static):
    
    def compose(self) -> ComposeResult:
        yield Label("Player Stats", id="stats-title")
        yield Label("HP: ---/---", id="stats-hp")
        yield Label("Level: 1", id="stats-level")
        yield Label("XP: 0/---", id="stats-xp")

class Sidebar(Container):

    def compose(self) -> ComposeResult:
        yield PlayerStats(classes="box")
        yield Label("Radar", classes="label")
        yield DirectoryTree(str(Path.home()), id="radar")

class RoomView(Container):

    def compose(self) -> ComposeResult:
        yield Label("Room View", classes="label")
        yield DataTable(id="room_table")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Name", "Type", "HP", "Size (Bytes)")
        table.cursor_type = "row"