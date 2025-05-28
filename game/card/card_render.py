from game.card.card_model import CardModel
from game.card.model_validator import ModelValidator


class CardRenderer:
    def __init__(self, model: CardModel):
        self.model = model

    def render(self) -> str:
        if not self.model.properties.basic:
            if self.model.properties.is_full:
                if self.model.properties.is_visible:
                    return (
                        f"[black on white]┌──────┐[/]\n"
                        f"[black on white]│[{ModelValidator.get_color(self.model.suit)}]{self.model.figure}{(' ' * (3 if self.model.figure == '10' else 4))}{self.model.suit}[black]│[/]\n"
                        f"[black on white]│      │[/]\n"
                        f"[black on white]│      │[/]\n"
                        f"[black on white]│      │[/]\n"
                        f"[black on white]│[{ModelValidator.get_color(self.model.suit)}]{self.model.suit}{(' ' * (3 if self.model.figure == '10' else 4))}{self.model.figure}[black]│[/]\n"
                        f"[black on white]└──────┘[/]"
                    )
                else:
                    return (
                        "[white on red]┌──────┐[/]\n"
                        "[white on red]│ ~~~~ │[/]\n"
                        "[white on red]│ GIGA │[/]\n"
                        "[white on red]│      │[/]\n"
                        "[white on red]│ THON │[/]\n"
                        "[white on red]│ ~~~~ │[/]\n"
                        "[white on red]└──────┘[/]"
                    )
            else:
                if not self.model.properties.is_visible:
                    return "[white on red]┌──────┐[/]\n[white on red]│~~~~~~│[/]\n"
                else:
                    return (
                        f"[black on white]┌──────┐[/]\n"
                        f"[black on white]│[{ModelValidator.get_color(self.model.suit)}]{self.model.figure}{(' ' * (3 if self.model.figure == '10' else 4))}{self.model.suit}[black]│[/]\n"
                    )
        elif self.model.properties.basic:
            if self.model.properties.is_full:
                return (
                    "[black on white]┌──────┐[/]\n"
                    "[black on white]│G    T│[/]\n"
                    "[black on white]│I    H│[/]\n"
                    "[black on white]│G    O│[/]\n"
                    "[black on white]│A    N│[/]\n"
                    "[black on white]│ ~~~~ │[/]\n"
                    "[black on white]└──────┘[/]"
                )
