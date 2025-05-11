from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label

from game.menu.Instructions import InstructionsScreen
from game.menu.Settings import SettingsScreen
from game.Board import GameScreen

class MainMenuScreen(Screen):
    game = False

    """The main menu screen for the Solitaire game."""
    BINDINGS = [
        Binding("escape", "request_quit", "Exit Game", show=True, priority=True)
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, name="Solitaire")
        with Container(id="main-menu-container"):
            yield Label("♠ ♥ SOLITAIRE ♦ ♣", id="menu-title")
            with Vertical(id="menu-options"):
                yield Button("New Game", id="new_game", variant="primary")
                yield Button("How to Play", id="how_to_play")
                # yield Button("High Scores", id="high_scores", variant="default")
                yield Button("Settings", id="settings")
                yield Button("Exit Game", id="exit_game", variant="error")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "new_game":
            self.app.push_screen(GameScreen())
        elif button_id == "how_to_play":
            self.app.push_screen(InstructionsScreen())
        elif button_id == "settings":
            self.app.push_screen(SettingsScreen())
        elif button_id == "exit_game":
            self.action_request_quit()

    def action_request_quit(self) -> None:
        self.app.exit(message="Thank you for playing Solitaire!")


class SolitaireApp(App[None]):

    CSS_PATH = ['../../src/menu.tcss', "../../src/board.tcss", '../../src/win.tcss']
    TITLE = "Solitaire"

    def on_mount(self) -> None:
        self.push_screen(MainMenuScreen())

if __name__ == "__main__":
    app = SolitaireApp()
    app.run()