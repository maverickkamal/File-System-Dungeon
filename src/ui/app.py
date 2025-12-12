from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DirectoryTree, DataTable
from textual.reactive import reactive
from pathlib import Path
from src.ui.widgets import Sidebar, RoomView
from src.engine.scanner import Scanner

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
    ]

    current_path = reactive(Path.home())

    def compose(self) -> ComposeResult:
        yield Header()
        yield Sidebar()
        yield RoomView()
        yield Footer()

    def on_mount(self) -> None:
        self.scan_current_room()

    def on_directory_tree_directory_selected(self, event: DirectoryTree.DirectorySelected) -> None:

        self.current_path = Path(event.path)
        self.scan_current_room()

    def scan_current_room(self) -> None:

        result = Scanner.scan_room(self.current_path)
        table = self.query_one(DataTable)
        table.clear()

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
        self.sub_title = str(self.current_path)
    
    def action_toggle_dark(self) -> None:
        self.dark = not self.dark