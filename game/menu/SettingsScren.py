from textual.app import App, ComposeResult
from textual.widgets import Switch, Header, Footer, Static, Select, Label
from textual.screen import Screen
from textual.containers import Grid
from textual.binding import Binding
from textual.widget import Widget
from game.Settings import Settings

class LabeledSwitch(Widget):
    """
    A switch with an accompanying label, styled and aligned in a grid.
    """
    def __init__(self, label_text: str, switch_name: str = "", *, value: bool = False) -> None:
        super().__init__(id=switch_name)
        self.label_text = label_text
        self.switch_name = switch_name
        self.value = value

    def compose(self) -> ComposeResult:
        yield Label(self.label_text, id=f"{self.switch_name}-label")
        yield Switch(value=self.value, name=self.switch_name, id=self.switch_name)

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings = Settings()

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back to Menu", show=True)
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        # A grid with two columns: labels & controls
        with Grid(id="settings-grid"):
            yield LabeledSwitch("Auto Shuffle", "auto_shuffle", value=self.settings.get("auto_shuffle"))
            yield LabeledSwitch("Hard Level", "hard_level", value=self.settings.get('hard_level'))
            yield Label("Auto Win Mode:", id="auto_win_label")
            yield Select(
                options=[
                    ("Always", "always"),
                    ("Ask", "ask"),
                    ("Never", "never")
                ],
                prompt="",
                value=f"{self.settings.get('auto_win_mode')}",
                id="auto_win_mode"
            )
            # Fourth row: language select
            yield Label("Language:", id="language_label")
            yield Select(
                options=[("English", "eng"), ("Polish", "pl")],
                prompt="",
                value=f"{self.settings.get('language')}",
                id="language"
            )
        yield Footer()

    def on_switch_changed(self, event: Switch.Changed) -> None:
        self.settings.change(event.switch.id, event.value)
        self.settings.save()

    def on_select_changed(self, event: Select.Changed) -> None:
        self.settings.change(event.select.id, event.value)
        self.settings.save()

