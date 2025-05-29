from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Static, Header, Footer
from game.translator import Translator


class InstructionsScreen(Screen):
    """Screen displaying game instructions with localization support.

    Attributes:
        translator (Translator): Handles translation of displayed text based on language code.

    Bindings:
        escape: Binds the Escape key to action that closes this screen and returns to the previous one.
    """

    BINDINGS = [Binding("escape", "app.pop_screen", "Back to Menu", show=True)]

    def __init__(self, language_code: str = 'en'):
        """Initializes the instructions screen with the specified language.

        Args:
            language_code (str): Language code for translations (default is 'en').
        """
        super().__init__()
        self.translator = Translator(language_code)

    def compose(self) -> ComposeResult:
        """Composes the UI elements of the instructions screen.

        Yields:
            ComposeResult: UI widgets to be rendered on this screen.
        """
        yield Header(name=self.translator.t("how_to_play"))
        with Container(classes="content-screen-container"):  # Main container for layout
            with ScrollableContainer(classes="content-box"):  # Scrollable area for instructions text
                yield Static(self.translator.t("how_to_play_title"), classes="content-title")
                yield Static(self.translator.t("how_to_play_text"), classes="content-text")
                with Vertical(classes="button-container-centered"):  # Centered button container
                    yield Button(self.translator.t("back_to_menu"), id="back_to_menu", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handles the button press event.

        If the back button is pressed, closes the instructions screen.

        Args:
            event (Button.Pressed): The button pressed event.
        """
        if event.button.id == "back_to_menu":
            self.app.pop_screen()
