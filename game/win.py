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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.width = self.size.height
        settings = Settings()
        self.language_code = settings.get("language", "en")
        self.translator = Translator(self.language_code)

    def _on_resize(self, event: events.Resize) -> None:
        self.width = self.size.height
        self.update_padding()

    def compose(self) -> ComposeResult:
        yield Center(
            Vertical(
                Static(self.translator.t("win_title"), id="title"),
                Static(self.translator.t("congratulations"), id="message"),
                Static(
                    f"{self.translator.t('time')}:\n{Timer.minutes}:{Timer.seconds} min\n{self.translator.t('score')}:\n{Score.score}",
                    id="information",
                ),
                Vertical(
                    Horizontal(
                        Vertical(
                            Button(self.translator.t("replay"), id="replay", variant="success")
                        ),
                        Vertical(Static(expand=True), id="row"),
                        Vertical(Button(self.translator.t("exit_btn"), id="exit", variant="error")),
                    ),
                    id="button-box",
                ),
                id="main-box",
            ),
            id="test",
        )

    def _on_mount(self, event: events.Mount) -> None:
        self.update_padding()

    def update_padding(self):
        box = self.query_one("#test")
        padding = self.width * 0.25
        padding = int(padding)
        box.styles.padding = padding

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "replay":
            self.app.push_screen(menu.MainMenuScreen())
        elif event.button.id == "exit":
            self.app.exit()
