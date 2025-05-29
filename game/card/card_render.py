from game.card.card_model import CardModel
from game.card.model_validator import ModelValidator


class CardRenderer:
    """Renders a card as a string based on its model properties."""

    def __init__(self, model: CardModel):
        """
        Initializes the renderer with a card model.

        Args:
            model (CardModel): The card model to render.
        """
        self.model = model

    def render(self) -> str:
        """
        Renders the card as a styled string depending on its properties.

        Returns:
            str: The rendered card as a string with formatting codes.
        """
        props = self.model.properties

        if props.basic:
            return self._render_basic(props.is_full)
        
        if not props.is_full:
            return self._render_half(props.is_visible)

        return self._render_full(props.is_visible)

    def _render_basic(self, is_full: bool) -> str:
        """Render basic mode card."""
        if not is_full:
            return "[black on white]┌──────┐[/]\n[black on white]│G    T│[/]"
        
        return (
            "[black on white]┌──────┐[/]\n"
            "[black on white]│G    T│[/]\n"
            "[black on white]│I    H│[/]\n"
            "[black on white]│G    O│[/]\n"
            "[black on white]│A    N│[/]\n"
            "[black on white]│ ~~~~ │[/]\n"
            "[black on white]└──────┘[/]"
        )

    def _render_half(self, is_visible: bool) -> str:
        """Render card that is not full size."""
        if not is_visible:
            return (
                "[white on red]┌──────┐[/]\n"
                "[white on red]│~~~~~~│[/]\n"
            )
        
        # Visible, half-size card
        figure = self.model.figure
        suit = self.model.suit
        color = ModelValidator.get_color(suit)
        spacing = ' ' * (3 if figure == '10' else 4)

        return (
            f"[black on white]┌──────┐[/]\n"
            f"[black on white]│[{color}]{figure}{spacing}{suit}[black]│[/]\n"
        )

    def _render_full(self, is_visible: bool) -> str:
        """Render full-size card (standard size)."""
        if not is_visible:
            return (
                "[white on red]┌──────┐[/]\n"
                "[white on red]│ ~~~~ │[/]\n"
                "[white on red]│ GIGA │[/]\n"
                "[white on red]│      │[/]\n"
                "[white on red]│ THON │[/]\n"
                "[white on red]│ ~~~~ │[/]\n"
                "[white on red]└──────┘[/]"
            )

        # Visible, full-size card
        figure = self.model.figure
        suit = self.model.suit
        color = ModelValidator.get_color(suit)
        spacing = ' ' * (3 if figure == '10' else 4)

        return (
            f"[black on white]┌──────┐[/]\n"
            f"[black on white]│[{color}]{figure}{spacing}{suit}[black]│[/]\n"
            f"[black on white]│      │[/]\n"
            f"[black on white]│      │[/]\n"
            f"[black on white]│      │[/]\n"
            f"[black on white]│[{color}]{suit}{spacing}{figure}[black]│[/]\n"
            f"[black on white]└──────┘[/]"
        )
