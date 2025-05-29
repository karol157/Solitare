from game.card.card_model import CardModel
from game.card import Card


class ModelValidator:
    """Validates whether a card move is legal based on Solitaire rules."""

    def __init__(self, main_model, model: CardModel):
        """
        Args:
            main_model: The UI card widget that owns this model.
            model (CardModel): The data model for the card.
        """
        self.main_model = main_model
        self.model = model

    @staticmethod
    def get_color(suit: str) -> str:
        """
        Get the color of a card based on its suit.

        Args:
            suit (str): Card suit, e.g., '♥', '♠'.

        Returns:
            str: 'red' for ♥ or ♦, 'black' otherwise.
        """
        return "red" if suit in "♥♦" else "black"

    def can_put_it_here(self) -> bool:
        """
        Determines if the selected card(s) can be placed on the target card according to Solitaire rules.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        '''rows, _, deck = self.main_model.parent_board.get_rows()

        # Card order from Ace to King
        cards_order = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

        try:
            # Get source card
            src_col = int(Card.Card.selected_allocation[0])
            src_pos = Card.Card.selected_allocation[1]
            source_from_stock = src_pos == "ST"
            src_idx = -1 if source_from_stock else int(src_pos)

            if source_from_stock:
                card_full = deck[src_col][-1]
            else:
                card_full = rows[src_col][src_idx]

            source_fig, source_suit = card_full[:-1], card_full[-1]

            # Get target
            tgt_col = int(self.main_model.allocation[0])
            target_type = self.model.properties.card_type

            if target_type == "D":
                # Foundation (suit pile)
                foundation = deck[tgt_col]
                if not foundation:
                    return source_fig == "A"
                top_full = foundation[-1]
                top_fig, top_suit = top_full[:-1], top_full[-1]
                return (
                    source_suit == top_suit
                    and cards_order.index(source_fig) == cards_order.index(top_fig) + 1
                )

            else:
                # Tableau (column)
                column = rows[tgt_col]
                if not column:
                    return source_fig == "K"
                top_full = column[-1]
                top_fig, top_suit = top_full[:-1], top_full[-1]
                return (
                    self.get_color(source_suit) != self.get_color(top_suit)
                    and cards_order.index(source_fig) + 1 == cards_order.index(top_fig)
                )

        except (IndexError, ValueError, KeyError):
            # Fail-safe: invalid allocation, missing cards, or corrupt data
            return False'''
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
        target_is_deck = self.main_model.allocation[1] == "D"
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
