from textual.app import App, ComposeResult
from textual.widgets import Switch, Header, Footer, Static, Select
from textual.screen import Screen

class SettingsScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("\nUstawienia\n", classes="bold")
        yield Switch("Auto Tasowanie", id="auto_shuffle")
        yield Select(
            options=[
                ("Zawsze", "always"),
                ("Pytaj", "ask"),
                ("Nigdy", "never")
            ],
            prompt="Auto Wygrana",
            id="auto_win_mode"
        )
        yield Footer()

    def on_switch_changed(self, event: Switch.Changed) -> None:
        self.app.settings[event.switch.id] = event.value

    def on_select_changed(self, event: Select.Changed) -> None:
        self.app.settings[event.select.id] = event.value

class SolitaireApp(App):
    CSS = """
    Screen {
        align: center middle;
        padding: 2;
    }
    """
    def on_mount(self) -> None:
        self.settings = {
            "auto_shuffle": False,
            "auto_win_mode": "ask"
        }
        self.push_screen(SettingsScreen())

if __name__ == "__main__":
    SolitaireApp().run()
