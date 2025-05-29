from game import undo
from game import Board
from game.card import Card
from game.Properties import Properties
from game.Settings import Settings
from game.Information import Score


class Mover:
    """Handles card movements within the game, including foundation, deck, and stock.

    Supports regular moves and undo operations, updates visual card widgets and game state.

    Methods:
        move: Main entry point to perform a move.
    """

    @staticmethod
    async def move(source: list, target: list, parent_board: Board, from_undo=False, visible_before=False):
        """Handles a card move between two containers.

        Args:
            source (list): Source allocation [row, index/type].
            target (list): Target allocation [row, index/type].
            parent_board (Board): Game board reference.
            from_undo (bool): Whether this move is part of an undo.
            visible_before (bool): Whether the card was visible before the move (undo support).
        """
        rows, properties, deck = parent_board.get_rows()
        from_stock = source[1] == "ST"
        from_deck = source[1] == "D"
        to_deck = target[1] == "D"
        to_stock = target[1] == "ST"

        # Prepare undo snapshot
        if not from_undo:
            undo_obj = undo.Undo(parent_board)
            undo_obj.add(source, target)

        # Decide which type of move to perform
        if from_stock:
            card = await Mover._move_from_stock(source, target, parent_board, deck, rows, properties, to_deck)
        elif from_undo and from_deck:
            score = Score()
            score.add(-15)
            if to_stock:
                card = await Mover._move_from_deck_to_stock_undo(source, target, parent_board, deck)
            else:
                card = await Mover._move_from_deck_to_foundation_undo(source, target, parent_board, deck, rows, properties)
        else:
            card = await Mover._move_within_foundation(source, target, parent_board, rows, properties)

        # Update UI and data for the target container
        target_container = await Mover._prepare_target_container(target, parent_board, to_deck, to_stock)
        await Mover._update_target_container(
            target_container,
            card,
            from_stock or (from_deck and to_stock),
            from_undo,
            from_deck,
            target,
            visible_before=visible_before,
        )

    # ------------------------
    # MOVE HANDLERS
    # ------------------------

    @staticmethod
    async def _move_from_stock(source, target, parent_board, deck, rows, properties, to_deck):
        """Handles movement of a card from the stock pile."""
        source_container = parent_board.query_one("#stock1")
        card_under_source = source_container.children[-1]

        card_data = deck[5][-1]
        card = [
            Card.Card(
                [card_data[:-1], card_data[-1]],
                Properties("g"),
                [int(target[0]), int(target[1]) if str(target[1]).isdigit() else "D"],
                parent_board,
            )
        ]
        card_under_source.remove()

        # Refresh stock with next visible card or placeholder
        if len(deck[5]) > 1:
            source_container.mount(
                Card.Card(
                    [deck[5][-2][:-1], deck[5][-2][-1]],
                    Properties("g"),
                    [5, "ST"],
                    parent_board,
                )
            )
        else:
            source_container.mount(
                Card.Card(
                    properties=Properties("s"),
                    allocation=[5, "ST"],
                    parent_board=parent_board,
                )
            )

        score = Score()
        if not to_deck:
            score.add(5)
            rows[target[0]].append(deck[5].pop())
            properties[int(target[0])].append("gfs")
        else:
            score.add(15)
            deck[target[0]].append(deck[5].pop())

        return card

    @staticmethod
    async def _move_from_deck_to_foundation_undo(source, target, parent_board, deck, rows, properties):
        """Undo: moves a card from the foundation back to the deck."""
        foundation_container = parent_board.query_one(f"#foundation{target[0]}")
        deck_container = parent_board.query_one(f"#deck{source[0]}")
        deck_container.remove_children()

        if len(deck[int(source[0])]) > 1:
            deck_container.mount(
                Card.Card(
                    [deck[int(source[0])][-2][:-1], deck[int(source[0])][-2][-1]],
                    Properties("d"),
                    allocation=[source[0], "D"],
                    parent_board=parent_board,
                )
            )
        else:
            deck_container.mount(
                Card.Card(
                    properties=Properties("d", order="f"),
                    allocation=[source[0], "D"],
                    parent_board=parent_board,
                )
            )

        data_card = deck[int(source[0])].pop()
        properties[target[0]].append("gfs")
        if len(properties[target[0]]) > 1:
            properties[target[-2]] = "gps"

        card = [
            Card.Card(
                [data_card[:-1], data_card[-1]],
                Properties("g"),
                [target[0], "G"],
                parent_board,
            )
        ]
        return card

    @staticmethod
    async def _move_from_deck_to_stock_undo(source, target, parent_board, deck):
        """Undo: moves a card from deck to stock."""
        deck_container = parent_board.query_one(f"#deck{source[0]}")
        stock_container = parent_board.query_one("#stock1")

        stock_container.remove_children()
        deck_container.remove_children()

        if len(deck[int(source[0])]) > 1:
            deck_container.mount(
                Card.Card(
                    [deck[int(source[0])][-2][:-1], deck[int(source[0])][-2][-1]],
                    Properties("d"),
                    allocation=[source[0], "D"],
                    parent_board=parent_board,
                )
            )
        else:
            deck_container.mount(
                Card.Card(
                    properties=Properties("d", order="f"),
                    allocation=[source[0], "D"],
                    parent_board=parent_board,
                )
            )

        if len(deck[int(source[0])]):
            card_data = deck[int(source[0])].pop()
            deck[5].append(card_data)
            card = [
                Card.Card(
                    [card_data[:-1], card_data[-1]],
                    Properties("g"),
                    [5, "ST"],
                    parent_board,
                )
            ]
        else:
            card = [
                Card.Card(
                    properties=Properties("ST", "f"),
                    allocation=[5, "ST"],
                    parent_board=parent_board,
                )
            ]
        return card

    @staticmethod
    async def _move_within_foundation(source, target, parent_board, rows, properties):
        """Moves card(s) between foundation piles or to deck/stock."""
        source_container = parent_board.query_one(f"#foundation{int(source[0])}")
        if source[1] == "x":
            source[1] = 0

        card = source_container.children[int(source[1]) :]
        card_under_source = source_container.children[int(source[1]) - 1]
        moving_cards = rows[source[0]][int(source[1]) :]
        moving_properties = properties[source[0]][int(source[1]) :]

        score = Score()
        if target[1] in ["D", "ST"]:
            if target[1] == "D":
                score.add(10)
            else:
                score.add(-15)
            _, _, deck = parent_board.get_rows()
            deck[target[0]].extend(moving_cards)
        else:
            rows[target[0]].extend(moving_cards)
            properties[target[0]].extend(moving_properties)

        del rows[source[0]][int(source[1]) :]
        del properties[source[0]][int(source[1]) :]

        # Replace with placeholder if nothing remains
        if not rows[source[0]]:
            source_container.mount(
                Card.Card(
                    properties=Properties("s"),
                    allocation=[source[0], "x"],
                    parent_board=parent_board,
                )
            )

        card_under_source.properties.is_full = True
        card_under_source.properties.is_visible = True
        card_under_source.update(card_under_source.card_render.render())
        card_under_source.can_focus = not Settings().get("mouse_control", False)

        return card

    # ------------------------
    # UI HELPERS
    # ------------------------

    @staticmethod
    async def _prepare_target_container(target, parent_board, to_deck, to_stock=False):
        """Returns container widget where the card should be placed."""
        if to_deck:
            container = parent_board.query_one(f"#deck{target[0]}")
            container.remove_children()
        elif to_stock:
            container = parent_board.query_one("#stock1")
        else:
            container = parent_board.query_one(f"#foundation{target[0]}")
        return container

    @staticmethod
    async def _update_target_container(
        target_container, card, from_stock, from_undo, from_deck, target, visible_before=False
    ):
        """Mounts the card(s) to the destination container and updates properties."""
        card_under_target = None

        if target[1] == "ST" and from_undo:
            target_container.remove_children()

        if hasattr(target_container, "children") and target_container.children:
            card_under_target = target_container.children[-1]

        if card_under_target and hasattr(card_under_target, "card_render"):
            if card_under_target.allocation[1] == "x":
                target_container.remove_children()
            else:
                card_under_target.properties.is_full = False
                card_under_target.properties.is_visible = visible_before if from_undo else True
                rendered = card_under_target.card_render.render()
                if rendered:
                    card_under_target.update(rendered)

        # Remove temp card widgets if not coming from stock/deck
        if not from_stock and not from_deck:
            for child in card:
                await child.remove()

        await target_container.mount(*card)

        for child in card:
            child.styles.offset = (0, 0)

        for index, child in enumerate(card):
            if target[1] == "x":
                target[1] = -1
            child.allocation = [
                target[0],
                ("D" if target[1] == "D" else (int(target[1]) + 1 + index)) if not from_undo
                else ("ST" if target[1] == "ST" else target[1] + index),
            ]
