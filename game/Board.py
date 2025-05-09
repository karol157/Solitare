from textual.binding import Binding
from textual.screen import Screen

from game.Card import Card
from game.Properties import Properties

import random
from textual.containers import Vertical, Horizontal
from textual.widget import Widget
from textual.widgets import Static, Footer
from textual.app import ComposeResult


class Board(Widget):
    row1 = []
    row2 = []
    row3 = []
    row4 = []
    row5 = []
    row6 = []
    row7 = []
    row1_properties = []
    row2_properties = []
    row3_properties = []
    row4_properties = []
    row5_properties = []
    row6_properties = []
    row7_properties = []
    desk_1 = []
    desk_2 = []
    desk_3 = []
    desk_4 = []
    stock1 = []
    stock2 = []
    def compose(self) -> ComposeResult:
        with Horizontal(id="table"):
            with Horizontal(id="stock"):
                for i in range(2):
                    with Vertical():
                        yield Card(properties=Properties('s', order='s'), parent_board=self, id=f"stock{i}")
            with Horizontal(id="deck"):
                for i in range(4):
                    with Vertical():
                        yield Card(properties=Properties('s'), allocation=[i, 'x'], parent_board=self, id=f"deck{i}")

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

    @staticmethod
    def random_card() -> None:
        rows, _, _ = Board.get_rows()
        cards = ['2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥', 'A♥', '2♠', '3♠', '4♠','5♠',
                '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠', 'A♠', '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦',
                '10♦', 'J♦', 'Q♦', 'K♦', 'A♦', '2♣', '3♣', '4♣', '5♣','6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣', 'A♣']

        for i, row in enumerate(rows, start=1):
            for _ in range(i):
                choice = random.choice(cards)
                row.append(choice)
                cards.remove(choice)

        Board.stock1 = cards

        random.shuffle(Board.stock1)

    @staticmethod
    def _generate_properties():
        rows, properties, _ = Board.get_rows()

        for i, row in enumerate(properties):
            if len(rows[i]) > 0:
                row.extend(["gph"] * (len(rows[i]) - 1))
                row.append("gfs")

    @staticmethod
    def get_rows():
        return [Board.row1, Board.row2,Board.row3,Board.row4,Board.row5,Board.row6,Board.row7], [Board.row1_properties, Board.row2_properties, Board.row3_properties, Board.row4_properties, Board.row5_properties, Board.row6_properties, Board.row7_properties],[Board.desk_1, Board.desk_2, Board.desk_3, Board.desk_4, Board.stock1, Board.stock2]

    @staticmethod
    def parse_to_property(value: str):
        card_type = value[0]
        is_full = value[1] == 'f'
        is_visible = value[2] == 's'
        return Properties(card_type, is_full, is_visible)

    @staticmethod
    def check_win():
        return (len(Board.desk_1) +len(Board.desk_2) +len(Board.desk_3) +len(Board.desk_4)) == 52

    @staticmethod
    def reset_game(board):
        rows, properties, deck = Board.get_rows()

        for i in rows:
            i.clear()
        for j in properties:
            j.clear()
        for k in deck:
            k.clear()
        Board.random_card()
        Board._generate_properties()
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
        board = self.query_one('#board')
        Board.reset_game(board)