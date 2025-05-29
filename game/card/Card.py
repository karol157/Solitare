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
    """UI widget representing a single playing card with interactivity and state."""

    selected = False
    selected_allocation = []

    def __init__(
        self,
        card: list = ["a", "♥"],
        properties: Properties = None,
        allocation: list = None,
        parent_board: Board = None,
        **kwargs,
    ):
        """
        Initialize a Card widget.

        Args:
            card (list): Card value and suit, e.g., ["a", "♥"].
            properties (Properties): Card state and flags.
            allocation (list): Location data on the board.
            parent_board (Board): Reference to the parent game board.
        """
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
        """Called when the widget is added to the UI. Renders the card."""
        self.update(self.card_render.render())

    def on_focus(self):
        """Style change on focus."""
        self.styles.border = ("round", "blue")

    def on_blur(self):
        """Reset style when focus is lost."""
        self.styles.border = "none"

    async def _on_key(self, event):
        """Handle keyboard input."""
        if event.key == "enter":
            await self.select()

    async def _on_click(self, event: events.Click) -> None:
        """Handle mouse click event."""
        await self.select()

    def _get_container_and_cards(self, allocation):
        """
        Retrieve container widget and its child cards based on allocation.

        Args:
            allocation (list): Allocation data [column, type].

        Returns:
            tuple: (container widget, list of card widgets)
        """
        if allocation[1] != "ST":
            container = self.parent_board.query_one(f"#foundation{allocation[0]}")
            cards = container.children[int(allocation[1]):]
        else:
            container = self.parent_board.query_one(f"#stock1")
            cards = container.children[-1:]
        return container, cards

    def _pick_up_cards(self):
        """Offset card(s) to indicate selection."""
        _, cards = self._get_container_and_cards(self.allocation)
        for child in cards:
            child.styles.offset = (0, 2)

    def _pick_down_cards(self):
        """Reset offset of selected cards."""
        _, cards = self._get_container_and_cards(Card.selected_allocation)
        for child in cards:
            child.styles.offset = (0, 0)

    def _reset_selection(self):
        """Deselect any selected cards."""
        self._pick_down_cards()
        Card.selected = False
        Card.selected_allocation.clear()

    async def select(self):
        """
        Main method for card selection and interaction logic.
        Handles selecting, moving, and flipping cards.
        """
        rows, properties, deck = self.parent_board.get_rows()
        score = Score()

        if Card.selected:
            # Attempt to place selected card on this one
            if not self.validator.can_put_it_here():
                self._reset_selection()
                return

            if (
                Card.selected_allocation[0] == self.allocation[0]
                and Card.selected_allocation[1] not in ["D", "ST"]
                and self.allocation[1] not in ["D", "ST"]
            ):
                self._reset_selection()
                return

            await self.mover.move(Card.selected_allocation, self.allocation, self.parent_board)

            if self.parent_board.check_win():
                if self.settings.get("auto_win_mode") == "ask":
                    button = self.app.screen.query_one("#auto_win")
                    button.display = True
                else:
                    self.app.push_screen(WinScreen())
                await self.parent_board.draw_card()
                return

            self._reset_selection()

        else:
            # If card is in the deck or stock, handle flipping logic
            if self.properties.card_type == "D" or (
                self.properties.card_type == "ST" and not deck[5]
            ):
                return

            elif self.properties.card_type == "STS" and deck[4]:
                score.add(5)

                if self.settings.get("hard_level"):
                    for _ in range(min(3, len(self.parent_board.stock1))):
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
                        Properties("st"),
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
                                properties=Properties("sts", is_visible=False),
                                allocation=[4, "STS"],
                                parent_board=self.parent_board,
                            )
                        )
                else:
                    score.add(-70 if self.settings.get("hard_level") else -20)
                    container.remove_children()
                    container.mount(
                        Card(
                            properties=Properties("sts", order="f"),
                            allocation=[4, "STS"],
                            parent_board=self.parent_board,
                        )
                    )

            elif self.properties.card_type == "STS" and not deck[4]:
                self.parent_board.stock1 = list(reversed(self.parent_board.stock2))
                self.parent_board.stock2 = []

                self.parent_board.query_one("#stock0").remove_children()
                self.parent_board.query_one("#stock0").mount(
                    Card(
                        properties=Properties("sts", is_visible=False),
                        allocation=[4, "STS"],
                        parent_board=self.parent_board,
                    )
                )

                self.parent_board.query_one("#stock1").remove_children()
                self.parent_board.query_one("#stock1").mount(
                    Card(
                        properties=Properties("s"),
                        allocation=[5, "ST"],
                        parent_board=self.parent_board,
                    )
                )

            elif self.properties.is_visible and not self.properties.basic:
                Card.selected = True
                Card.selected_allocation = [
                    self.allocation[0],
                    self.allocation[-1],
                ]
                self._pick_up_cards()

    def set_card(self, card: str, properties: str = "gph"):
        """
        Set or update the card's value and properties.

        Args:
            card (str): Card string like "A♠".
            properties (str): Properties flags.
        """
        self.model.figure = card[0].upper()
        self.model.suit = card[1]
        self.model.properties = properties
        self.update(self.card_render.render())

    def update_row_properties(self):
        """
        Update internal property strings for all board rows.
        Adds `p` to cards in row to mark as 'playable', last one as 'face-up'.
        """
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
                prop_row[-1] = "gfs"  # mark last card as face-up

class Card(Static):
    """UI widget representing a single playing card with interactivity and state."""

    selected = False
    selected_allocation = []

    def __init__(
        self,
        card: list = ["a", "♥"],
        properties: Properties = None,
        allocation: list = None,
        parent_board: Board = None,
        **kwargs,
    ):
        """
        Initialize a Card widget.

        Args:
            card (list): Card value and suit, e.g., ["a", "♥"].
            properties (Properties): Card state and flags.
            allocation (list): Location data on the board.
            parent_board (Board): Reference to the parent game board.
        """
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
        """Called when the widget is added to the UI. Renders the card."""
        self.update(self.card_render.render())

    def on_focus(self):
        """Style change on focus."""
        self.styles.border = ("round", "blue")

    def on_blur(self):
        """Reset style when focus is lost."""
        self.styles.border = "none"

    async def _on_key(self, event):
        """Handle keyboard input."""
        if event.key == "enter":
            await self.select()

    async def _on_click(self, event: events.Click) -> None:
        """Handle mouse click event."""
        await self.select()

    def _get_container_and_cards(self, allocation):
        """
        Retrieve container widget and its child cards based on allocation.

        Args:
            allocation (list): Allocation data [column, type].

        Returns:
            tuple: (container widget, list of card widgets)
        """
        if allocation[1] != "ST":
            container = self.parent_board.query_one(f"#foundation{allocation[0]}")
            cards = container.children[int(allocation[1]):]
        else:
            container = self.parent_board.query_one(f"#stock1")
            cards = container.children[-1:]
        return container, cards

    def _pick_up_cards(self):
        """Offset card(s) to indicate selection."""
        _, cards = self._get_container_and_cards(self.allocation)
        for child in cards:
            child.styles.offset = (0, 2)

    def _pick_down_cards(self):
        """Reset offset of selected cards."""
        _, cards = self._get_container_and_cards(Card.selected_allocation)
        for child in cards:
            child.styles.offset = (0, 0)

    def _reset_selection(self):
        """Deselect any selected cards."""
        self._pick_down_cards()
        Card.selected = False
        Card.selected_allocation.clear()

    async def select(self):
        """
        Main method for card selection and interaction logic.
        Handles selecting, moving, and flipping cards.
        """
        rows, properties, deck = self.parent_board.get_rows()
        score = Score()

        if Card.selected:
            # Attempt to place selected card on this one
            if not self.validator.can_put_it_here():
                self._reset_selection()
                return

            if (
                Card.selected_allocation[0] == self.allocation[0]
                and Card.selected_allocation[1] not in ["D", "ST"]
                and self.allocation[1] not in ["D", "ST"]
            ):
                self._reset_selection()
                return

            await self.mover.move(Card.selected_allocation, self.allocation, self.parent_board)

            if self.parent_board.check_win():
                if self.settings.get("auto_win_mode") == "ask":
                    button = self.app.screen.query_one("#auto_win")
                    button.display = True
                else:
                    self.app.push_screen(WinScreen())
                await self.parent_board.draw_card()
                return

            self._reset_selection()

        else:
            # If card is in the deck or stock, handle flipping logic
            if self.properties.card_type == "D" or (
                self.properties.card_type == "ST" and not deck[5]
            ):
                return

            elif self.properties.card_type == "STS" and deck[4]:
                score.add(5)

                if self.settings.get("hard_level"):
                    for _ in range(min(3, len(self.parent_board.stock1))):
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
                        Properties("st"),
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
                                properties=Properties("sts", is_visible=False),
                                allocation=[4, "STS"],
                                parent_board=self.parent_board,
                            )
                        )
                else:
                    score.add(-70 if self.settings.get("hard_level") else -20)
                    container.remove_children()
                    container.mount(
                        Card(
                            properties=Properties("sts", order="f"),
                            allocation=[4, "STS"],
                            parent_board=self.parent_board,
                        )
                    )

            elif self.properties.card_type == "STS" and not deck[4]:
                self.parent_board.stock1 = list(reversed(self.parent_board.stock2))
                self.parent_board.stock2 = []

                self.parent_board.query_one("#stock0").remove_children()
                self.parent_board.query_one("#stock0").mount(
                    Card(
                        properties=Properties("sts", is_visible=False),
                        allocation=[4, "STS"],
                        parent_board=self.parent_board,
                    )
                )

                self.parent_board.query_one("#stock1").remove_children()
                self.parent_board.query_one("#stock1").mount(
                    Card(
                        properties=Properties("s"),
                        allocation=[5, "ST"],
                        parent_board=self.parent_board,
                    )
                )

            elif self.properties.is_visible and not self.properties.basic:
                Card.selected = True
                Card.selected_allocation = [
                    self.allocation[0],
                    self.allocation[-1],
                ]
                self._pick_up_cards()

    def set_card(self, card: str, properties: str = "gph"):
        """
        Set or update the card's value and properties.

        Args:
            card (str): Card string like "A♠".
            properties (str): Properties flags.
        """
        self.model.figure = card[0].upper()
        self.model.suit = card[1]
        self.model.properties = properties
        self.update(self.card_render.render())

    def update_row_properties(self):
        """
        Update internal property strings for all board rows.
        Adds `p` to cards in row to mark as 'playable', last one as 'face-up'.
        """
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
                prop_row[-1] = "gfs"  # mark last card as face-up
