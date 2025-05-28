from textual import events
from textual.widgets import Static

from game import Board
from game.Properties import Properties
from game.win import WinScreen
from game.Settings import Settings
from game.card.card_render import CardRenderer
from game.card.card_model import CardModel
from game.card.model_validator import ModelValidator
from game.card.mover import Mover
from game.Information import Score


class Card(Static):
    selected = False
    selected_allocation = []

    def __init__(
        self,
        card: list = ["a", "♥"],
        properties: Properties = None,
        allocation: list = None,
        parent_board: Board = None,
        **kwargs,
    ):  #  ♥,♠,♦,♣
        super().__init__(**kwargs)
        self.figure = card[0].upper()
        self.color = card[1]
        self.properties = properties
        self.allocation = allocation if allocation is not None else []
        self.parent_board = parent_board
        self.model = CardModel(self.figure, self.color, self.properties)
        self.validator = ModelValidator(self, self.model)
        self.card_render = CardRenderer(self.model)
        self.settings = Settings()
        self.mover = Mover()

        if (
            self.properties.is_visible or self.properties.card_type == "STS"
        ) and not self.settings.get("mouse_control", False):
            self.can_focus = True

    def on_mount(self):
        self.update(self.card_render.render())

    def on_focus(self):
        self.styles.border = ("round", "blue")

    async def _on_key(self, event):
        if event.key == "enter":
            await self.select()

    def on_blur(self):
        self.styles.border = "none"

    async def select(self):
        def reset_selection():
            pick_down_cards()
            Card.selected = False
            Card.selected_allocation.clear()

        def pick_up_cards():
            if self.allocation[1] != "ST":
                container = self.parent_board.query_one(
                    f"#foundation{self.allocation[0]}"
                )
                card = container.children[int(self.allocation[1]) :]
            else:
                container = self.parent_board.query_one(f"#stock1")
                card = container.children[-1:]
            for child in card:
                child.styles.offset = (0, 2)

        def pick_down_cards():
            if Card.selected_allocation[1] != "ST":
                container = self.parent_board.query_one(
                    f"#foundation{Card.selected_allocation[0]}"
                )
                card = container.children[int(Card.selected_allocation[1]) :]
            else:
                container = self.parent_board.query_one(f"#stock1")
                card = container.children[-1:]
            for child in card:
                child.styles.offset = (0, 0)

        rows, properties, deck = self.parent_board.get_rows()
        score = Score()
        if Card.selected:
            if not self.validator.can_put_it_here():
                reset_selection()
                return
            if (
                Card.selected_allocation[0] == self.allocation[0]
                and Card.selected_allocation[1] not in ["D", "ST"]
                and self.allocation[1] not in ["D", "ST"]
            ):
                reset_selection()
                return

            await self.mover.move(
                Card.selected_allocation, self.allocation, self.parent_board
            )

            if self.parent_board.check_win():
                if self.settings.get("auto_win_mode") == "ask":
                    game_screen = self.app.screen
                    button = game_screen.query_one("#auto_win")
                    button.display = True
                else:
                    self.app.push_screen(WinScreen())
                await self.parent_board.draw_card()
                return

            reset_selection()
        else:
            if self.properties.card_type == "D" or (
                self.properties.card_type == "ST" and not deck[5]
            ):
                return
            elif self.properties.card_type == "STS" and deck[4]:
                score.add(5)
                if self.settings.get("hard_level"):
                    move_count = min(3, len(self.parent_board.stock1))
                    for _ in range(move_count):
                        self.parent_board.stock2.append(self.parent_board.stock1.pop())
                else:
                    self.parent_board.stock2.append(self.parent_board.stock1.pop())

                if not self.parent_board.stock1 and self.settings.get("auto_shuffle"):
                    self.parent_board.stock1 = list(reversed(self.parent_board.stock2))
                    self.parent_board.stock2 = []

                container = self.parent_board.query_one("#stock1")
                container.remove_children()
                container.mount(
                    Card(
                        [deck[5][-1][:-1], deck[5][-1][-1]],
                        (Properties("st")),
                        [5, "ST"],
                        self.parent_board,
                    )
                )
                container = self.parent_board.query_one("#stock0")
                if self.parent_board.stock1:
                    if container.children[-1].properties.is_visible:
                        container.remove_children()
                        container.mount(
                            Card(
                                properties=(Properties("sts", is_visible=False)),
                                allocation=[4, "STS"],
                                parent_board=self.parent_board,
                            )
                        )
                else:
                    if self.settings.get("hard_level"):
                        score.add(-70)
                    else:
                        score.add(-20)
                    container = self.parent_board.query_one("#stock0")
                    container.remove_children()
                    container.mount(
                        Card(
                            properties=(Properties("sts", order='f')),
                            allocation=[4, "STS"],
                            parent_board=self.parent_board,
                        )
                    )
            else:
                if self.properties.card_type == "STS" and not deck[4]:
                    self.parent_board.stock1 = list(reversed(self.parent_board.stock2))
                    self.parent_board.stock2 = []
                    container = self.parent_board.query_one("#stock0")
                    container.remove_children()
                    container.mount(
                        Card(
                            properties=(Properties("sts", is_visible=False)),
                            allocation=[4, "STS"],
                            parent_board=self.parent_board,
                        )
                    )
                    container = self.parent_board.query_one("#stock1")
                    container.remove_children()
                    container.mount(
                        Card(
                            properties=(Properties("s")),
                            allocation=[5, "ST"],
                            parent_board=self.parent_board,
                        )
                    )
                else:
                    if self.properties.is_visible and not self.properties.basic:
                        Card.selected = True
                        Card.selected_allocation = [
                            self.allocation[0],
                            self.allocation[-1],
                        ]
                        pick_up_cards()

    async def _on_click(self, event: events.Click) -> None:
        await self.select()

    def set_card(self, card: str, properties: str = "gph"):
        self.model.figure = card[0].upper()
        self.model.suit = card[1]
        self.model.properties = properties

        self.update(self.card_render.render())

    def update_row_properties(self):
        properties = [
            self.parent_board.row1_properties,
            self.parent_board.row2_properties,
            self.parent_board.row3_properties,
            self.parent_board.row4_properties,
            self.parent_board.row5_properties,
            self.parent_board.row6_properties,
            self.parent_board.row7_properties,
        ]

        for prop_row in properties:
            for i, index in enumerate(prop_row):
                prop_row[i] = f"{prop_row[i][0]}p{prop_row[i][2]}"
            if prop_row:
                prop_row[-1] = "gfs"
