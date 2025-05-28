from game.card import mover
'''class Undo:
    moves = []

    def __init__(self, board):
        self.board = board
        self.mover = mover.Mover()

    def add(self, source: list, target: list):
        # Save a copy, not a reference
        source_copy = list(source)
        target_copy = list(target)
        target_copy[1] = (
            str(int(target_copy[1]) + 1)
            if str(target_copy[1]).isdigit()
            else target_copy[1]
        )
        if len(Undo.moves) < 3:
            Undo.moves.append([source_copy, target_copy])
        else:
            del Undo.moves[0]
            Undo.moves.append([source_copy, target_copy])

    async def undo(self):
        if len(Undo.moves) > 0:
            last_move = Undo.moves[-1]
            await self.mover.move(
                last_move[1], last_move[0], self.board, from_undo=True
            )
            Undo.moves.pop()
        else:
            return False

    def clear(self):
        Undo.moves.clear()
'''

class Undo:
    moves = []
    def __init__(self, board):
        self.board = board
        self.mover = mover.Mover()
    
    def add(self, source: list, target: list):
        # Pobierz kontener targetu i stan widoczności karty pod targetem
        container = self.board.query_one(f"#foundation{source[0]}" if source[1] not in ['D','ST'] else ("#stock1" if source[1]=='ST' else f"#deck{source[0]}"))
        if len(container.children) > 1:
            card_under = container.children[-2]
            visible_before = card_under.properties.is_visible
        else:
            visible_before = True

        # Przygotuj kopie źródła i celu
        source_copy = list(source)
        target_copy = list(target)
        target_copy[1] = str(int(target_copy[1]) + 1) if str(target_copy[1]).isdigit() else target_copy[1]
        record = [source_copy, target_copy, visible_before]

        if len(Undo.moves) < 3:
            Undo.moves.append(record)
        else:
            del Undo.moves[0]
            Undo.moves.append(record)

    async def undo(self):
        if Undo.moves:
            source, target, visible_before = Undo.moves.pop()
            # Swap source and target for undo
            await self.mover.move(target, source, self.board, from_undo=True, visible_before=visible_before)
        else:
            return False
    
    def clear(self):
        Undo.moves.clear()
