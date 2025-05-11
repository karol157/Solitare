from textual import events
from textual.binding import Binding
from textual.screen import Screen

from game.Card import Card
from game.Properties import Properties
from game import Information
from game.win import WinScreen

import random
from textual.containers import Vertical, Horizontal
from textual.widget import Widget
from textual.widgets import Static, Footer
from textual.app import ComposeResult


class Board(Widget):
    def __init__(self ,**kwargs):
        super().__init__(**kwargs)
        self.row1 = []
        self.row2 = []
        self.row3 = []
        self.row4 = []
        self.row5 = []
        self.row6 = []
        self.row7 = []
        self.row1_properties = []
        self.row2_properties = []
        self.row3_properties = []
        self.row4_properties = []
        self.row5_properties = []
        self.row6_properties = []
        self.row7_properties = []
        self.desk_1 = []
        self.desk_2 = []
        self.desk_3 = []
        self.desk_4 = []
        self.stock1 = []
        self.stock2 = []
    def compose(self) -> ComposeResult:
        with Horizontal(id="table"):
            with Horizontal(id="stock"):
                for i in range(2):
                    with Vertical(id=f"stock{i}"):
                        yield Card(properties=Properties('s', order='s'), parent_board=self)
            with Horizontal(id="Information"):
                yield Information.Information(id="Information-object")
            with Horizontal(id="deck"):
                for i in range(5):
                    with Vertical(id=f"deck{i}"):
                        yield Card(properties=Properties('s'), allocation=[i, 'x'], parent_board=self)

        yield Vertical(
            Static(id="divider"),
        )
        with Horizontal(id="foundations"):
            for j in range(7):
                with Vertical(id=f"foundation{j}"):
                    yield Card(properties=Properties('s'))

    def on_mount(self):
        Board.reset_game(self)

    def draw_card(self):
        rows, properties, decks = self.get_rows()

        for i, row in enumerate(rows):
            container = self.query_one(f"#foundation{i}", Vertical)
            if not row:
                container.remove_children()
                container.mount(Card(properties=Properties('s'), allocation=[i, 'x'], parent_board=self))
            else:
                container.remove_children()
                for index, card_str in enumerate(row):
                    card = Card(['10' if card_str[0] == '1' else card_str[0],card_str[-1]],
                                self.parse_to_property(properties[i][index]),
                                [i, index], self)
                    if Card.selected:
                        if (Card.selected_allocation[1] != 'ST' and Card.selected_allocation[1] != 'D') and int(i) == int(Card.selected_allocation[0]) and int(index) >= int(Card.selected_allocation[1]):
                            card.styles.offset = (0,2)
                        else:
                            card.styles.offset = (0,0)
                    container.mount(card)

        for i, deck in enumerate(decks):
            if i < 4:
                container = self.query_one(f"#deck{i}")
                if not deck:
                    container.remove_children()
                    container.mount(Card(properties=Properties('d', order='f'), allocation=[i, 'D'], parent_board=self))
                else:
                    container.remove_children()
                    container.mount(Card([deck[-1][:-1],deck[-1][-1]], properties=Properties('d'), allocation=[i, 'D'], parent_board=self))
            else:
                container = self.query_one(f"#stock{i - 4}")
                if not deck:
                    container.remove_children()
                    container.mount(Card(properties=Properties(('st' if i == 5 else 'sts'), order='f'), allocation=[i, ('ST' if i == 5 else 'STS')], parent_board=self))
                else:
                    container.remove_children()
                    top = deck[-1]
                    card = [top[:-1], top[-1]]
                    card_obj = Card(card ,properties=Properties(('st' if i == 5 else 'sts'), is_visible=(i==5)), allocation=[i, ('ST' if i == 5 else 'STS')], parent_board=self)
                    if Card.selected and i == 5 and Card.selected_allocation[1] == "ST":
                        card_obj.styles.offset = (0,2)
                    else:
                        card_obj.styles.offset = (0,0)
                    container.mount(card_obj)

    def random_card(self) -> None:
        rows, _, _ = self.get_rows()
        cards = ['2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥', 'A♥', '2♠', '3♠', '4♠','5♠',
                '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠', 'A♠', '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦',
                '10♦', 'J♦', 'Q♦', 'K♦', 'A♦', '2♣', '3♣', '4♣', '5♣','6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣', 'A♣']

        for i, row in enumerate(rows, start=1):
            for _ in range(i):
                choice = random.choice(cards)
                row.append(choice)
                cards.remove(choice)

        self.stock1 = cards

        random.shuffle(self.stock1)

    def generate_properties(self):
        rows, properties, _ = self.get_rows()

        for i, row in enumerate(properties):
            if len(rows[i]) > 0:
                row.extend(["gph"] * (len(rows[i]) - 1))
                row.append("gfs")

    def get_rows(self):
        return [self.row1, self.row2,self.row3,self.row4,self.row5,self.row6,self.row7], [self.row1_properties, self.row2_properties, self.row3_properties, self.row4_properties, self.row5_properties, self.row6_properties, self.row7_properties],[self.desk_1, self.desk_2, self.desk_3, self.desk_4, self.stock1, self.stock2]

    @staticmethod
    def parse_to_property(value: str):
        card_type = value[0]
        is_full = value[1] == 'f'
        is_visible = value[2] == 's'
        return Properties(card_type, is_full, is_visible)

    def check_win(self):
        return (len(self.desk_1) +len(self.desk_2) +len(self.desk_3) +len(self.desk_4)) == 52

    @staticmethod
    def reset_game(board):
        rows, properties, deck = board.get_rows()

        information = board.query_one("#Information-object")
        information.reset()

        for i in rows:
            i.clear()
        for j in properties:
            j.clear()
        for k in deck:
            k.clear()
        board.random_card()
        board.generate_properties()
        board.draw_card()


class GameScreen(Screen):
    """Displays game instructions."""
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back to Menu", show=True), Binding("r", "reset_game", "Reset Game", show=True)
    ]
    def compose(self) -> ComposeResult:
        self.styles.background = 'green'
        self.mount(Board(id="board"))
        yield Footer()

    def action_reset_game(self):
        board = self.query_one('#board', Board)
        Board.reset_game(board)