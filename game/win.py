from textual import events
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Vertical, Center, Horizontal

from game.menu import menu
from game.Information import Score, Timer
from game.Settings import Settings
from game.translator import Translator


class WinScreen(Screen):
    """
    Screen displayed when the player wins the game.

    Shows game stats (time and score) and options to replay or exit.
    """

    def __init__(self, **kwargs):
        """
        Initialize the WinScreen instance and set up language translation.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the base Screen class.
        """
        super().__init__(**kwargs)
        self.width = self.size.height  # Initial width based on screen height
        settings = Settings()
        self.language_code = settings.get("language", "en")
        self.translator = Translator(self.language_code)

    def _on_resize(self, event: events.Resize) -> None:
        """
        Called on window resize event to adjust padding dynamically.

        Args:
            event (events.Resize): The resize event.
        """
        self.width = self.size.height
        self.update_padding()

    def compose(self) -> ComposeResult:
        """
        Compose the user interface components for the WinScreen.

        Yields:
            ComposeResult: The UI widgets and containers for this screen.
        """
        yield Center(
            Vertical(
                Static(self.translator.t("win_title"), id="title"),
                Static(self.translator.t("congratulations"), id="message"),
                Static(
                    f"{self.translator.t('time')}:\n{Timer.minutes}:{Timer.seconds} min\n"
                    f"{self.translator.t('score')}:\n{Score.score}",
                    id="information",
                ),
                Vertical(
                    Horizontal(
                        Vertical(
                            Button(self.translator.t("replay"), id="replay", variant="success")
                        ),
                        Vertical(Static(expand=True), id="row"),
                        Vertical(
                            Button(self.translator.t("exit_btn"), id="exit", variant="error")
                        ),
                    ),
                    id="button-box",
                ),
                id="main-box",
            ),
            id="test",
        )

    def _on_mount(self, event: events.Mount) -> None:
        """
        Called when the screen is mounted; updates padding accordingly.

        Args:
            event (events.Mount): The mount event.
        """
        self.update_padding()

    def update_padding(self):
        """
        Update padding of the main container based on current screen width.

        Adjusts the padding proportionally to the width for better layout.
        """
        box = self.query_one("#test")
        padding = int(self.width * 0.25)
        box.styles.padding = padding

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handle button pressed events for the replay and exit buttons.

        Args:
            event (Button.Pressed): The button press event.
        """
        if event.button.id == "replay":
            self.app.push_screen(menu.MainMenuScreen())
        elif event.button.id == "exit":
            self.app.exit()
