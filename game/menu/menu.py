from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label

from game.menu.Instructions import InstructionsScreen
from game.menu.SettingsScren import SettingsScreen
from game.Board import GameScreen
from game.music import MusicPlayer
from game.Settings import Settings
from game.translator import Translator
import os


class MainMenuScreen(Screen):
    """
    The main menu screen for the Solitaire game.

    Displays menu options: New Game, How to Play, Settings, Exit Game,
    and handles music playback and navigation.

    Attributes:
        settings (Settings): Global settings instance.
        translator (Translator): Handles localization based on settings.
        music (MusicPlayer): Background music player instance.
    """

    game = False
    settings = Settings()
    translator = Translator(settings.get("language", "en"))  # Use language from settings

    # Key binding: Escape key requests to quit the app
    BINDINGS = [
        Binding("escape", "request_quit", "Exit Game", show=True, priority=True)
    ]

    # Initialize menu music if enabled in settings
    if settings.get("music", False):
        path = os.path.join("musics", "menu.wav")
        music = MusicPlayer(path, id="menu")
        music.start()

    def compose(self) -> ComposeResult:
        """Compose the main menu UI elements.

        Returns:
            ComposeResult: The UI widgets to render.
        """
        yield Header(show_clock=True, name=self.translator.t("solitaire"))
        with Container(id="main-menu-container"):
            yield Label(self.translator.t("menu_title"), id="menu-title")
            with Vertical(id="menu-options"):
                yield Button(self.translator.t("new_game"), id="new_game", variant="primary")
                yield Button(self.translator.t("how_to_play"), id="how_to_play")
                yield Button(self.translator.t("settings"), id="settings")
                yield Button(self.translator.t("exit_game"), id="exit_game", variant="error")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events on the main menu.

        Args:
            event (Button.Pressed): Button press event.
        """
        button_id = event.button.id
        if button_id == "new_game":
            # Stop menu music and start game music if music enabled
            if MainMenuScreen.settings.get("music", False):
                MainMenuScreen.music.stop()
                music = MusicPlayer(os.path.join("musics", "game.wav"), id="game")
                music.start()
            self.app.push_screen(GameScreen())
        elif button_id == "how_to_play":
            # Show instructions screen with current language
            self.app.push_screen(InstructionsScreen(language_code=self.translator.language_code))
        elif button_id == "settings":
            # Show settings screen
            self.app.push_screen(SettingsScreen())
        elif button_id == "exit_game":
            self.action_request_quit()

    def action_request_quit(self) -> None:
        """Exit the application gracefully."""
        self.app.exit(message="Thank you for playing Solitaire!")


class SolitaireApp(App[None]):
    """Main application class for Solitaire.

    Responsible for initializing and mounting the main menu screen.
    """

    CSS_PATH = [
        "../../src/menu.tcss",
        "../../src/board.tcss",
        "../../src/win.tcss",
        "../../src/settings.tcss",
    ]
    TITLE = "Solitaire"

    def on_mount(self) -> None:
        """Push the main menu screen on app start."""
        self.push_screen(MainMenuScreen())


if __name__ == "__main__":
    app = SolitaireApp()
    app.run()
