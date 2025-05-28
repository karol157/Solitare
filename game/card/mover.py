# -*- coding: utf-8 -*-
from game import undo
from game import Board
from game.card import Card
from game.Properties import Properties
from game.Settings import Settings
from game.Information import Score


class Mover:
    @staticmethod
    async def move(source: list, target: list, parent_board: Board, from_undo=False, visible_before=False):
        rows, properties, deck = parent_board.get_rows()
        from_stock = source[1] == "ST"
        from_deck = source[1] == "D"
        to_deck = target[1] == "D"
        to_stock = target[1] == "ST"

        undo_obj = undo.Undo(parent_board)
        if not from_undo:
            undo_obj.add(source, target)

        if from_stock:
            card = await Mover._move_from_stock(
                source, target, parent_board, deck, rows, properties, to_deck
            )
        elif from_undo and from_deck:
            score = Score()
            score.add(-15)
            if to_stock:
                card = await Mover._move_from_deck_to_stock_undo(
                    source, target, parent_board, deck
                )
            else:
                card = await Mover._move_from_deck_to_foundation_undo(
                    source, target, parent_board, deck, rows, properties
                )
        else:
            card = await Mover._move_within_foundation(
                source, target, parent_board, rows, properties
            )

        target_container = await Mover._prepare_target_container(
            target, parent_board, to_deck, to_stock
        )
        await Mover._update_target_container(
            target_container,
            card,
            from_stock or (from_deck and to_stock),
            from_undo,
            from_deck,
            target,
            visible_before=visible_before,
        )

    @staticmethod
    async def _move_from_foundation_to_stock_undo(source, target, parent_board):
        source_container = parent_board.query_one(f"#foundation{source[1]}")
        card = source_container.children[-1]

        card.properties = Properties("ST")

        return card

    @staticmethod
    async def _move_from_deck_to_foundation_undo(
        source, target, parent_board, deck, rows, properties
    ):
        # Remove card from foundation and put it back to deck
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
            # If there are no more cards in the deck, mount an empty card
            deck_container.mount(
                Card.Card(
                    properties=Properties("d", order="f"),
                    allocation=[source[0], "D"],
                    parent_board=parent_board,
                )
            )

        data_card = deck[int(source[0])].pop()
        _, properties, _ = parent_board.get_rows()
        properties[target[0]].append("gfs")
        if len(properties[target[0]]) > 1:
            properties[target[-2]] = "gps"

        # Create the card widget for foundation
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
    async def _move_from_stock(
        source, target, parent_board, deck, rows, properties, to_deck
    ):
        source_container = parent_board.query_one("#stock1")
        card_under_source = source_container.children[-1]
        card = [
            Card.Card(
                [deck[int(source[0])][-1][:-1], deck[int(source[0])][-1][-1]],
                Properties("g"),
                [int(target[0]), int(target[1]) if str(target[1]).isdigit() else "D"],
                parent_board,
            )
        ]
        card_under_source.remove()
        if len(deck[5]) > 1:
            source_container.mount(
                Card.Card(
                    [deck[5][-2][:-1], deck[5][-2][-1]] if deck[5] else ["A", "x"],
                    Properties("g") if deck[5] else Properties("s"),
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
    async def _move_from_deck_to_stock_undo(source, target, parent_board, deck):
        # Only for undo: move card from deck back to stock
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
            # If there are no more cards in the deck, mount an empty card
            deck_container.mount(
                Card.Card(
                    properties=Properties("d", order="f"),
                    allocation=[source[0], "D"],
                    parent_board=parent_board,
                )
            )

        # Move card data from deck to stock
        if len(deck[int(source[0])]):
            card_data = deck[int(source[0])].pop()
            deck[5].append(card_data)
            # Create the card widget for stock
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
    async def _prepare_target_container(target, parent_board, to_deck, to_stock=False):
        if to_deck:
            target_container = parent_board.query_one(f"#deck{target[0]}")
            target_container.remove_children()
        elif to_stock:
            target_container = parent_board.query_one("#stock1")
            # Optionally clear and prepare stock container if needed
        else:
            target_container = parent_board.query_one(f"#foundation{target[0]}")
        return target_container

    @staticmethod
    async def _move_within_foundation(source, target, parent_board, rows, properties):
        source_container = parent_board.query_one(f"#foundation{int(source[0])}")
        if source[1] == "x":
            source[1] = 0
        card = source_container.children[int(source[1]) :]
        card_under_source = source_container.children[int(source[1]) - 1]
        moving_cards = rows[source[0]][int(source[1]) :]
        moving_properties = properties[source[0]][int(source[1]) :]

        score = Score()

        # Check if moving to deck
        if target[1] == "D" or target[1] == "ST":
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
        settings = Settings()
        if settings.get("mouse_control", False):
            card_under_source.can_focus = False
        else:
            card_under_source.can_focus = True
        return card

    @staticmethod
    async def _prepare_target_container(target, parent_board, to_deck, to_stock=False):
        if to_deck:
            target_container = parent_board.query_one(f"#deck{target[0]}")
            target_container.remove_children()
        elif to_stock:
            target_container = parent_board.query_one("#stock1")
        else:
            target_container = parent_board.query_one(f"#foundation{target[0]}")
        return target_container

    @staticmethod
    async def _update_target_container(
        target_container, card, from_stock, from_undo, from_deck, target, visible_before=False
    ):
        # Only update card_under_target if it exists and has a valid render
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
                if from_undo:
                    score = Score()
                    score.add(-15)
                    card_under_target.properties.is_visible = visible_before
                else:
                    card_under_target.properties.is_visible = True
                rendered = card_under_target.card_render.render()
                if rendered is not None:
                    card_under_target.update(rendered)

        if not from_stock and not from_deck:
            for child in card:
                await child.remove()

        await target_container.mount(*card)
        for child in card:
            child.styles.offset = (0, 0)
        for index, child in enumerate(card):
            if target[1] == "x":
                target[1] = -1
            if not from_undo:
                child.allocation = [
                    target[0],
                    ("D" if target[1] == "D" else (int(target[1]) + 1 + index)),
                ]
            else:
                child.allocation = [
                    target[0],
                    ("ST" if target[1] == "ST" else target[1] + index),
                ]
