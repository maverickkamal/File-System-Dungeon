from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Placeholder

class FileSystemDungeonApp(App):
    """A TUI RPG Explorer for navigating the file system."""

    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
        grid-columns: 1fr 3fr;
    }
    """

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Placeholder("Sidebar (Stats & Radar)", id="sidebar")
        yield Placeholder("Room View (Files)", id="room_view")
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle on dark mode """

        self.dark = not self.dark

if __name__ == "__main__":
    app = FileSystemDungeonApp()
    app.run()