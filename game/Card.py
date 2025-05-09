from textual import events

from game import Board
from game.Properties import Properties

from textual.widgets import Static

class Card(Static):
    selected = False
    selected_allocation = []
    def __init__(self, card: list=['a', '♥'], properties: Properties=None, allocation: list=[], parent_board: Board =None, **kwargs): #  ♥,♠,♦,♣
        super().__init__(**kwargs)
        self.figure = card[0].upper()
        self.color = card[1]
        self.properties = properties
        self.allocation = allocation
        self.parent_board = parent_board

    def on_mount(self):
        self.update(self.create_card())

    def create_card(self):

        if not self.properties.basic:
            if self.properties.is_full:
                if self.properties.is_visible:
                    return (
                        f"[black on white]┌──────┐[/]\n"
                        f"[black on white]│[{self.get_color(self.color)}]{self.figure}{(' ' * (3 if self.figure == '10' else 4))}{self.color}[black]│[/]\n"
                        f"[black on white]│      │[/]\n"
                        f"[black on white]│      │[/]\n"
                        f"[black on white]│      │[/]\n"
                        f"[black on white]│[{self.get_color(self.color)}]{self.color}{(' ' * (3 if self.figure == '10' else 4))}{self.figure}[black]│[/]\n"
                        f"[black on white]└──────┘[/]"
                    )
                else:
                    return (
                        f"[white on red]┌──────┐[/]\n"
                        f"[white on red]│ ~~~~ │[/]\n"
                        f"[white on red]│ GIGA │[/]\n"
                        f"[white on red]│      │[/]\n"
                        f"[white on red]│ THON │[/]\n"
                        f"[white on red]│ ~~~~ │[/]\n"
                        f"[white on red]└──────┘[/]"
                    )
            else:
                if not self.properties.is_visible:
                    return (
                        f"[white on red]┌──────┐[/]\n"
                        f"[white on red]│~~~~~~│[/]\n"
                    )
                else:
                    return (
                        f"[black on white]┌──────┐[/]\n"
                        f"[black on white]│[{self.get_color(self.color)}]{self.figure}{(' ' * (3 if self.figure == '10' else 4))}{self.color}[black]│[/]\n"
                    )
        elif self.properties.basic:
            if self.properties.is_full:
                return (
                    f"[black on white]┌──────┐[/]\n"
                    f"[black on white]│G    T│[/]\n"
                    f"[black on white]│I    H│[/]\n"
                    f"[black on white]│G    O│[/]\n"
                    f"[black on white]│A    N│[/]\n"
                    f"[black on white]│ ~~~~ │[/]\n"
                    f"[black on white]└──────┘[/]"
                )


    def _on_click(self, event: events.Click) -> None:
        rows, properties, deck = Board.Board.get_rows()

        event.stop()

        if Card.selected:
            if not self.can_put_it_here():
                Card.selected = False
                Card.selected_allocation.clear()
                self.parent_board.draw_card()
                return

            if Card.selected_allocation[0] == self.allocation[0] and Card.selected_allocation[1] not in ['D', 'ST'] and self.allocation[1] not in ['D', 'ST']:
                with open('file.txt', 'a') as f:
                    f.write(f"{str(self.allocation)} + {str(Card.selected_allocation)}\n")
                self.styles.offset = (0, 0)
                Card.selected = False
                Card.selected_allocation.clear()
            else:
                target_row = int(self.allocation[0])
                if str(Card.selected_allocation[1]).isdigit():
                    source_index = int(Card.selected_allocation[1])
                else:
                    source_index = -1
                source_row = int(Card.selected_allocation[0])

                if self.properties.card_type == 'D':
                    if not self.can_put_it_here():
                        Card.selected = False
                        Card.selected_allocation.clear()
                        self.parent_board.draw_card()
                        return

                    source_row = int(Card.selected_allocation[0])

                    if Card.selected_allocation[1] == 'ST':
                        deck[int(self.allocation[0])].append(deck[5].pop())
                    elif str(Card.selected_allocation[1]).isdigit():
                        card = rows[source_row].pop()
                        properties[source_row].pop()
                        deck[int(self.allocation[0])].append(card)
                        try:
                            properties[source_row][-1] = 'gfs'
                        except IndexError:
                            pass

                    Card.selected = False
                    Card.selected_allocation.clear()
                    self.parent_board.draw_card()
                    return

                if Card.selected_allocation[1] == 'ST' and source_row == 5: #Stock
                    if self.can_put_it_here():
                        rows[target_row].append(deck[5].pop())
                        properties[target_row].append('gfs')
                        try:
                            properties[target_row][-2] = 'gps'
                        except IndexError:
                            pass
                        Card.selected = False
                        Card.selected_allocation.clear()
                        self.parent_board.draw_card()
                        return
                    else:
                        Card.selected = False
                        Card.selected_allocation.clear()
                        self.parent_board.draw_card()
                        return
                if str(Card.selected_allocation[1]).isdigit(): #Normal card
                    moving_cards = rows[source_row][source_index:]
                    moving_properties = properties[source_row][source_index:]
                    rows[target_row].extend(moving_cards)
                    properties[target_row].extend(moving_properties)
                    del rows[source_row][source_index:]
                    del properties[source_row][source_index:]

                Card.selected = False
                Card.selected_allocation.clear()
                self.styles.offset = (0, 0)
        else:
            if self.properties.card_type == 'D' or (self.properties.card_type == 'ST' and not deck[5]):
                return
            if self.properties.card_type == 'STS' and deck[4]:
                Board.Board.stock2.append(Board.Board.stock1.pop())
                self.parent_board.draw_card()
                return
            else:
                if self.properties.card_type == 'STS' and not deck[4]:
                    Board.Board.stock1 = list(reversed(Board.Board.stock2))
                    Board.Board.stock2 = []
                    self.parent_board.draw_card()
                else:
                    if self.properties.is_visible and not self.properties.basic:
                        Card.selected = True
                        Card.selected_allocation = [self.allocation[0], self.allocation[-1]]
                        self.styles.offset = (0, 2)

        self.update_row_properties()
        self.parent_board.draw_card()


    def set_card(self, card: str, properties: str='gph'):
        self.figure = card[0].upper()
        self.color = card[1]
        self.properties = properties

        self.update(self.create_card())
    @staticmethod
    def update_row_properties():
        properties = [
            Board.Board.row1_properties, Board.Board.row2_properties, Board.Board.row3_properties,
            Board.Board.row4_properties, Board.Board.row5_properties, Board.Board.row6_properties,
            Board.Board.row7_properties
        ]

        for prop_row in properties:
            for i, index in enumerate(prop_row):
                prop_row[i] = f'{prop_row[i][0]}p{prop_row[i][2]}'
            if prop_row:
                prop_row[-1] = 'gfs'

    @staticmethod
    def get_color(suit):
        """
        Returns the color of a card based on its suit.

        Hearts ('♥') and Diamonds ('♦') are red; Clubs ('♣') and Spades ('♠') are black.

        Args:
            suit (str): A single-character string representing the suit of the card.

        Returns:
            str: 'red' if the suit is ♥ or ♦, 'black' otherwise.
        """
        return 'red' if suit in '♥♦' else 'black'
    def can_put_it_here(self) -> bool:
        """
        Determines whether the selected card can be placed onto the target row.

        The method checks if the move is legal according to Solitaire rules:
        - A card can be placed on another card if it is one rank lower and of the opposite color.
        - A King ('K') can be placed on an empty row.

        Returns:
            bool: True if the selected card can be placed on the target row, False otherwise.
        """
        rows, _, deck = Board.Board.get_rows()
        cards_order = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']

        src_row = int(Card.selected_allocation[0])
        src_alloc = Card.selected_allocation[1]
        source_from_stack = (src_alloc == 'ST')
        src_idx = -1 if source_from_stack else int(src_alloc)

        if source_from_stack:
            card_full = deck[src_row][-1]
        else:
            card_full = rows[src_row][src_idx]

        source_fig, source_suit = card_full[:-1], card_full[-1]


        tgt_row = int(self.allocation[0])
        target_is_deck = (self.properties.card_type == 'D')
        if target_is_deck:
            foundation = deck[tgt_row]
            if not foundation:
                return source_fig == 'A'
            top_full = foundation[-1]
            top_fig, top_suit = top_full[:-1], top_full[-1]
            return (
                source_suit == top_suit
                and cards_order.index(source_fig) == cards_order.index(top_fig) + 1
            )
        else:
            column = rows[tgt_row]
            if not column:
                return source_fig == 'K'
            top_full = column[-1]
            top_fig, top_suit = top_full[:-1], top_full[-1]
            return (
                self.get_color(source_suit) != self.get_color(top_suit)
                and cards_order.index(source_fig) + 1 == cards_order.index(top_fig)
            )
