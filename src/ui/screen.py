from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, Button, Static
from textual.containers import Grid, Horizontal, Vertical, Container

class CombatModal(ModalScreen):

    CSS = """
    CombatModal {
        align: center middle;
    }

    #dialog {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1fr 3fr;
        padding: 0 1;
        width: 60;
        height: 11;
        border: thick $background 80%;
        background: $surface;
    }

    #question {
        column-span: 2;
        height: 1fr;
        width: 1fr;
        content-align: center middle;
    }

    #stats {
        column-span: 2;
        height: 1fr;
        width: 1fr;
        content-align: center middle;
        text-align: center;
    }

    #buttons {
        column-span: 2;
        height: auto;
        width: 1fr;
        align: center bottom;
    }

    Button {
        width: 3%;
        margin: 0 1;
    }
    """

    def __init__(self, entity_data: dict):
        super().__init__()
        self.entity_data = entity_data

    def compose(self) -> ComposeResult:
        with Grid(id="dialog"):
            yield Label(f"ENCOUNTER: {self.entity_data['name']}", id="question")

            stats_text = (
                f"Type: {self.entity_data['type']}\n"
                f"HP: {self.entity_data['hp']} / {self.entity_data['max_hp']}\n"
                f"Size: {self.entity_data['size_bytes']} bytes"
            )
            yield Label(stats_text, id="stats")

            with Horizontal(id="buttons"):
                yield Button("Attack", variant="error", id="btn_attack")
                yield Button("Inspect", variant="primary", id="btn_inspect")
                yield Button("Run", variant="default", id="btn_run")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_run":
            self.dismiss("run")
        elif event.button.id == "btn_attack":
            self.dismiss("attack")
        elif event.button.id == "btn_inspect":
            self.dismiss("inspect")