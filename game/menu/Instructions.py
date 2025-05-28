from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Static, Header, Footer
from game.translator import Translator


class InstructionsScreen(Screen):
    """Displays game instructions."""

    BINDINGS = [Binding("escape", "app.pop_screen", "Back to Menu", show=True)]

    def __init__(self, language_code='en'):
        super().__init__()
        self.translator = Translator(language_code)

    def compose(self) -> ComposeResult:
        yield Header(name=self.translator.t("how_to_play"))
        with Container(classes="content-screen-container"):  # Use the new container
            with ScrollableContainer(classes="content-box"):
                yield Static(self.translator.t("how_to_play_title"), classes="content-title")
                yield Static(self.translator.t("how_to_play_text"), classes="content-text")
                with Vertical(classes="button-container-centered"):
                    yield Button(self.translator.t("back_to_menu"), id="back_to_menu", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back_to_menu":
            self.app.pop_screen()
