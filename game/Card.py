from textual import events
from textual.widgets import Static


from game import Board
from game.Properties import Properties
from game.win import WinScreen
from game.Settings import Settings
from time import sleep

class CardModel:
    def __init__(self, figure: str, suit: str, properties: Properties):
        self.figure = figure.upper()
        self.suit = suit
        self.properties = properties


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
                        f"[white on red]┌──────┐[/]\n"
                        f"[white on red]│ ~~~~ │[/]\n"
                        f"[white on red]│ GIGA │[/]\n"
                        f"[white on red]│      │[/]\n"
                        f"[white on red]│ THON │[/]\n"
                        f"[white on red]│ ~~~~ │[/]\n"
                        f"[white on red]└──────┘[/]"
                    )
            else:
                if not self.model.properties.is_visible:
                    return (
                        f"[white on red]┌──────┐[/]\n"
                        f"[white on red]│~~~~~~│[/]\n"
                    )
                else:
                    return (
                        f"[black on white]┌──────┐[/]\n"
                        f"[black on white]│[{ModelValidator.get_color(self.model.suit)}]{self.model.figure}{(' ' * (3 if self.model.figure == '10' else 4))}{self.model.suit}[black]│[/]\n"
                    )
        elif self.model.properties.basic:
            if self.model.properties.is_full:
                return (
                    f"[black on white]┌──────┐[/]\n"
                    f"[black on white]│G    T│[/]\n"
                    f"[black on white]│I    H│[/]\n"
                    f"[black on white]│G    O│[/]\n"
                    f"[black on white]│A    N│[/]\n"
                    f"[black on white]│ ~~~~ │[/]\n"
                    f"[black on white]└──────┘[/]"
                )


class ModelValidator:
    def __init__(self, main_model, model: CardModel):
        self.main_model = main_model
        self.model = model
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
        rows, _, deck = self.main_model.parent_board.get_rows()
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


        tgt_row = int(self.main_model.allocation[0])
        target_is_deck = (self.model.properties.card_type == 'D')
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
        self.model = CardModel(self.figure, self.color, self.properties)
        self.validator = ModelValidator(self, self.model)
        self.card_render = CardRenderer(self.model)
        self.settings = Settings()

    def on_mount(self):
        self.update(self.card_render.render())

    def _on_click(self, event: events.Click) -> None:
        def reset_selection():
            self.styles.offset = (0, 0)
            Card.selected = False
            Card.selected_allocation.clear()
            self.update_row_properties()
            self.parent_board.draw_card()

        rows, properties, deck = self.parent_board.get_rows()

        event.stop()

        if Card.selected:
            if not self.validator.can_put_it_here():
                reset_selection()
                return

            if Card.selected_allocation[0] == self.allocation[0] and Card.selected_allocation[1] not in ['D', 'ST'] and self.allocation[1] not in ['D', 'ST']:
                reset_selection()
                return
            else:
                target_row = int(self.allocation[0])
                if str(Card.selected_allocation[1]).isdigit():
                    source_index = int(Card.selected_allocation[1])
                else:
                    source_index = -1
                source_row = int(Card.selected_allocation[0])

                if self.properties.card_type == 'D':
                    if not self.validator.can_put_it_here():
                        reset_selection()
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
                    if self.parent_board.check_win():
                        self.app.push_screen(WinScreen())
                    self.parent_board.draw_card()
                    return

                if Card.selected_allocation[1] == 'ST' and source_row == 5: #Stock
                    if self.validator.can_put_it_here():
                        rows[target_row].append(deck[5].pop())
                        properties[target_row].append('gfs')
                        try:
                            properties[target_row][-2] = 'gps'
                        except IndexError:
                            pass
                        reset_selection()
                        return
                    else:
                        reset_selection()
                        return
                if str(Card.selected_allocation[1]).isdigit(): #Normal card
                    moving_cards = rows[source_row][source_index:]
                    moving_properties = properties[source_row][source_index:]

                    rows[target_row].extend(moving_cards)
                    properties[target_row].extend(moving_properties)

                    del rows[source_row][source_index:]
                    del properties[source_row][source_index:]


                reset_selection()
                self.styles.offset = (0, 0)
        else:
            if self.properties.card_type == 'D' or (self.properties.card_type == 'ST' and not deck[5]):
                self.parent_board.draw_card()
                return
            elif self.properties.card_type == 'STS' and deck[4]:
                if self.settings.get("hard_level"):
                    move_count = min(3, len(self.parent_board.stock1))
                    for _ in range(move_count):
                        self.parent_board.stock2.append(self.parent_board.stock1.pop())
                else:
                    self.parent_board.stock2.append(self.parent_board.stock1.pop())
                
                if not self.parent_board.stock1 and self.settings.get("auto_shuffle"):
                    self.parent_board.stock1 = list(reversed(self.parent_board.stock2))
                    self.parent_board.stock2 = []
                self.parent_board.draw_card()
                return
            else:
                if self.properties.card_type == 'STS' and not deck[4]:
                    self.parent_board.stock1 = list(reversed(self.parent_board.stock2))
                    self.parent_board.stock2 = []
                else:
                    if self.properties.is_visible and not self.properties.basic:
                        Card.selected = True
                        Card.selected_allocation = [self.allocation[0], self.allocation[-1]]
                        self.styles.offset = (0, 2) 

            self.update_row_properties()
            self.parent_board.draw_card()


    def set_card(self, card: str, properties: str='gph'):
        self.model.figure = card[0].upper()
        self.model.suit = card[1]
        self.model.properties = properties

        self.update(self.card_render.render())
    def update_row_properties(self):
        properties = [
            self.parent_board.row1_properties, self.parent_board.row2_properties, self.parent_board.row3_properties,
            self.parent_board.row4_properties, self.parent_board.row5_properties, self.parent_board.row6_properties,
            self.parent_board.row7_properties
        ]

        for prop_row in properties:
            for i, index in enumerate(prop_row):
                prop_row[i] = f'{prop_row[i][0]}p{prop_row[i][2]}'
            if prop_row:
                prop_row[-1] = 'gfs'
