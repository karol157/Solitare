from textual import events
from textual.app import ComposeResult, App
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Vertical, Center, Horizontal

from game.menu import menu
from game.Information import Score, Timer

class WinScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.width = self.size.height

    def _on_resize(self, event: events.Resize) -> None:
        self.width = self.size.height
        self.update_padding()

    def compose(self) -> ComposeResult:
        yield Center(
            Vertical(
                Static("- WIN -", id="title"),
                Static("Congratulations", id="message"),
                Static(f"Time:\n{Timer.minutes}:{Timer.seconds} min\nScore:\n{Score.score}", id="information"),
                Vertical(
                    Horizontal(Vertical( Button("Back To Menu", id="replay", variant="success")),
                               Vertical(Static(expand=True), id="row"),
                               Vertical(Button("Wyjdź", id="exit", variant="error"))),
                    id="button-box"
                ),
                id="main-box"
            ),
            id="test"
        )
    def _on_mount(self, event: events.Mount) -> None:
        self.update_padding()

    def update_padding(self):
        box = self.query_one("#test")
        padding = (self.width * 0.25)
        padding = int(padding)
        box.styles.padding = padding

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "replay":
            self.app.push_screen(menu.MainMenuScreen())
        elif event.button.id == "exit":
            self.app.exit()