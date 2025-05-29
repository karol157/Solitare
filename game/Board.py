from textual.binding import Binding
from textual.screen import Screen
from textual.containers import Vertical, Horizontal
from textual.widget import Widget
from textual.widgets import Static, Footer, Button
from textual.app import ComposeResult
from textual import events

from game.card.Card import Card
from game.Properties import Properties
from game import Information
from game.Settings import Settings
from game.win import WinScreen
from game.undo import Undo
from game.music import MusicPlayer

import os
import random
import asyncio


class Board(Widget):
    """Board class , represents the game board.

    Args:
        Widget (Widget): This class is widget
    """

    def __init__(self, **kwargs):
        """class init function."""
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

        self.settings = Settings()

    def compose(self) -> ComposeResult:
        """creating the board layout.

        Yields:
            Iterator[ComposeResult]: Widget objects
        """
        with Horizontal(id="table"):
            with Horizontal(id="stock"):
                for i in range(2):
                    with Vertical(id=f"stock{i}"):
                        yield Card(
                            properties=Properties("s", order="s"), parent_board=self
                        )
            with Horizontal(id="Information"):
                yield Information.Information(id="Information-object")
            with Horizontal(id="deck"):
                for i in range(4):
                    with Vertical(id=f"deck{i}"):
                        yield Card(
                            properties=Properties("s"),
                            allocation=[i, "x"],
                            parent_board=self,
                        )

        yield Vertical(
            Static(id="divider"),
        )
        with Horizontal(id="foundations"):
            for j in range(7):
                with Vertical(id=f"foundation{j}"):
                    yield Card(properties=Properties("s"))

    async def on_mount(self):
        """code to run when the board is mounted"""
        rows, properties, deck = self.get_rows()

        information = self.query_one("#Information-object")
        information.reset()

        undo_obj = Undo(self)
        undo_obj.clear()

        for i in rows + properties + deck:
            i.clear()

        Card.selected = False
        Card.selected_allocation.clear()
        self.random_card()
        self.generate_properties()
        await self.draw_card()

    async def draw_foundation(self, force_redraw):
        """draws the foundation cards"""
        rows, properties, _ = self.get_rows()
        colors = {"♥": "hearts", "♠": "spades", "♦": "diamonds", "♣": "clubs"}

        for i, row in enumerate(rows):
            cards = []
            container = self.query_one(f"#foundation{i}", Vertical)
            await asyncio.gather(*(child.remove() for child in container.children))
            if not row:
                container.mount(
                    Card(
                        properties=Properties("s"),
                        allocation=[i, "x"],
                        parent_board=self,
                    )
                )
            else:
                for index, card_str in enumerate(row):
                    card = Card(
                        [card_str[:-1], card_str[-1]],
                        self.parse_to_property(properties[i][index]),
                        [i, index],
                        self,
                        id=f"card_{card_str[:-1]}_{colors.get(card_str[-1])}",
                    )
                    if Card.selected:
                        if (
                            (
                                Card.selected_allocation[1] != "ST"
                                and Card.selected_allocation[1] != "D"
                            )
                            and int(i) == int(Card.selected_allocation[0])
                            and int(index) >= int(Card.selected_allocation[1])
                        ):
                            card.styles.offset = (0, 2)
                        else:
                            card.styles.offset = (0, 0)
                    cards.append(card)
                await container.mount(*cards)

    @staticmethod
    async def reset_game(board):
        """resets the game state"""
        await board.app.action_reload()

    def draw_deck(self):
        """draw cards from deck"""
        _, _, decks = self.get_rows()
        for i in range(4):
            container = self.query_one(f"#deck{i}", Vertical)
            container.remove_children()
            if not decks[i]:
                container.mount(
                    Card(
                        properties=Properties("d", order="f"),
                        allocation=[i, "D"],
                        parent_board=self,
                    )
                )
            else:
                container.mount(
                    Card(
                        [decks[i][-1][:-1], decks[i][-1][-1]],
                        properties=Properties("d"),
                        allocation=[i, "D"],
                        parent_board=self,
                    )
                )

    def draw_stock(self):
        """draw cards form stock"""
        _, _, stock = self.get_rows()

        for i in range(4, 6):
            container = self.query_one(f"#stock{i - 4}", Vertical)
            container.remove_children()
            if not stock[i]:
                container.mount(
                    Card(
                        properties=Properties("d", order="f"),
                        allocation=[i, "D"],
                        parent_board=self,
                    )
                )
            else:
                card_obj = Card(
                    [stock[i][-1][:-1], stock[i][-1][-1]],
                    properties=Properties(
                        ("st" if i == 5 else "sts"), is_visible=(i == 5)
                    ),
                    allocation=[i, ("ST" if i == 5 else "STS")],
                    parent_board=self,
                )
                if Card.selected and i == 5 and Card.selected_allocation[1] == "ST":
                    card_obj.styles.offset = (0, 2)
                else:
                    card_obj.styles.offset = (0, 0)
                container.mount(card_obj)

    async def draw_card(self, force_redraw: bool = False):
        """draw cards on the board"""
        await self.draw_foundation(force_redraw)
        self.draw_deck()
        self.draw_stock()

    def random_card(self):
        rows, _, _ = self.get_rows()
        cards = [
            f"{v}{s}"
            for s in "♥♠♦♣"
            for v in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        ]
        for i, row in enumerate(rows, start=1):
            for _ in range(i):
                choice = random.choice(cards)
                row.append(choice)
                cards.remove(choice)
        self.stock1 = cards
        random.shuffle(self.stock1)

    def generate_properties(self) -> None:
        rows, props, _ = self.get_rows()
        for i, row in enumerate(rows):
            props[i].extend(["gph"] * (len(row) - 1))
            props[i].append("gfs")

    def get_rows(self) -> list:
        return (
            [
                self.row1,
                self.row2,
                self.row3,
                self.row4,
                self.row5,
                self.row6,
                self.row7,
            ],
            [
                self.row1_properties,
                self.row2_properties,
                self.row3_properties,
                self.row4_properties,
                self.row5_properties,
                self.row6_properties,
                self.row7_properties,
            ],
            [
                self.desk_1,
                self.desk_2,
                self.desk_3,
                self.desk_4,
                self.stock1,
                self.stock2,
            ],
        )

    @staticmethod
    def parse_to_property(value: str) -> Properties:
        card_type = value[0]
        is_full = value[1] == "f"
        is_visible = value[2] == "s"
        return Properties(card_type, is_full, is_visible)

    def check_win(self) -> bool:
        _, properties, _ = self.get_rows()
        if self.settings.get("auto_win_mode") == "never":
            return (
                len(self.desk_1)
                + len(self.desk_2)
                + len(self.desk_3)
                + len(self.desk_4)
            ) == 52
        for i in range(7):
            container = self.query_one(f"#foundation{i}", Vertical)
            for child in container.children:
                if not child.properties.is_visible:
                    return False

        return True


class GameScreen(Screen):
    """Displays game instructions."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = self.app.size.height
        self.width = self.app.size.width

    BINDINGS = [
        Binding("escape", "back_to_menu", "Back to Menu", show=True),
        Binding("r", "reset_game", "Reset Game", show=True),
        Binding("u", "undo", "Undo", show=True),
    ]

    def action_back_to_menu(self) -> None:
        self.app.pop_screen()
        settings = Settings()
        if settings.get("music", False):
            music = MusicPlayer(
                "musics/game.wav", id="local"
            )  # get instance of music, attribute is not used only for the sake of consistency
            music_menu = music.get_instance("menu")
            music_game = music.get_instance("game")

            music_game.stop()
            music_menu.start()

    def compose(self) -> ComposeResult:
        self.styles.background = "green"
        yield Board(id="board")
        yield Button("Auto Win", id="auto_win")
        yield Footer()

    def on_mount(self):
        button = self.query_one("#auto_win")
        button.display = False

    async def action_reset_game(self):
        await self.app.pop_screen()
        await self.app.push_screen(GameScreen())

    async def action_undo(self):
        board = self.query_one("#board")
        undo_obj = Undo(board)
        await undo_obj.undo()

    def on_resize(self, event: events.Resize) -> None:
        self.width = self.app.size.width
        button = self.query_one("#auto_win")
        margin_left = (self.width / 2) - 14
        button.styles.margin = (0, 0, 2, int(margin_left))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "auto_win":
            self.app.push_screen(WinScreen())
