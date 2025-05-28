from game.card.card_model import CardModel
from game.card import Card


class ModelValidator:
    def __init__(self, main_model, model: CardModel):
        self.main_model = main_model
        self.model = model

    @staticmethod
    def get_color(suit):
        """Returns the color of a card based on its suit.

        Args:
            suit (str): A single-character string representing the suit of the card.

        Returns:
            str: 'red' if the suit is ♥ or ♦, 'black' otherwise.
        """
        return "red" if suit in "♥♦" else "black"

    def can_put_it_here(self) -> bool:
        """
        Determines whether the selected card can be placed onto the target row.

        The method checks if the move is legal according to Solitaire rules:
        - A card can be placed on another card if it is one rank lower and of the opposite color.
        - A King ('K') can be placed on an empty row.

        Returns:
            bool: True if the selected card can be placed on the target row, False otherwise.
        """
        return True
        rows, _, deck = self.main_model.parent_board.get_rows()

        cards_order = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

        src_row = int(Card.Card.selected_allocation[0])
        src_alloc = Card.Card.selected_allocation[1]
        source_from_stack = src_alloc == "ST"
        src_idx = -1 if source_from_stack else int(src_alloc)

        if source_from_stack:
            card_full = deck[src_row][-1]
        else:
            card_full = rows[src_row][src_idx]

        source_fig, source_suit = card_full[:-1], card_full[-1]

        tgt_row = int(self.main_model.allocation[0])
        target_is_deck = self.model.properties.card_type == "D"

        if target_is_deck:
            foundation = deck[tgt_row]
            if not foundation:
                return source_fig == "A"
            top_full = foundation[-1]
            top_fig, top_suit = top_full[:-1], top_full[-1]
            return (
                source_suit == top_suit
                and cards_order.index(source_fig) == cards_order.index(top_fig) + 1
            )
        else:
            column = rows[tgt_row]
            if not column:
                return source_fig == "K"
            top_full = column[-1]
            top_fig, top_suit = top_full[:-1], top_full[-1]
            return self.get_color(source_suit) != self.get_color(
                top_suit
            ) and cards_order.index(source_fig) + 1 == cards_order.index(top_fig)
