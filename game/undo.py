from game.card import mover

class Undo:
    """
    Class to handle undoing moves in a card game.
    
    Keeps track of the last 3 moves and allows reverting them.
    """

    moves = []  # Class-level list storing recent moves (up to 3)

    def __init__(self, board):
        """
        Initialize Undo with a reference to the game board and a mover instance.

        Args:
            board: The game board object that contains card containers and UI elements.
        """
        self.board = board
        self.mover = mover.Mover()

    def add(self, source: list, target: list):
        """
        Add a move to the undo stack.

        Args:
            source (list): The original position of the moved card.
            target (list): The new position of the moved card.
        """
        # Determine container related to the source, based on card type
        container = self.board.query_one(
            f"#foundation{source[0]}"
            if source[1] not in ['D', 'ST']
            else ("#stock1" if source[1] == 'ST' else f"#deck{source[0]}")
        )

        # Check if there is a card under the moved card and save its visibility state
        if len(container.children) > 1:
            card_under = container.children[-2]
            visible_before = card_under.properties.is_visible
        else:
            visible_before = True

        # Make copies of source and target to avoid reference issues
        source_copy = list(source)
        target_copy = list(target)
        # Adjust target's second element if it's numeric by incrementing by 1
        target_copy[1] = str(int(target_copy[1]) + 1) if str(target_copy[1]).isdigit() else target_copy[1]

        # Prepare record to save including visibility of the underlying card
        record = [source_copy, target_copy, visible_before]

        # Keep only the last 3 moves
        if len(Undo.moves) < 3:
            Undo.moves.append(record)
        else:
            del Undo.moves[0]
            Undo.moves.append(record)

    async def undo(self):
        """
        Undo the last move by swapping source and target and using the mover.

        Returns:
            bool: False if no moves to undo, otherwise None.
        """
        if Undo.moves:
            source, target, visible_before = Undo.moves.pop()
            # Call mover to move the card back with flag indicating undo and visibility state
            await self.mover.move(target, source, self.board, from_undo=True, visible_before=visible_before)
        else:
            return False

    def clear(self):
        """
        Clear all saved moves in the undo stack.
        """
        Undo.moves.clear()
