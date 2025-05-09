from game.menu.menu import SolitaireApp

'''from game.Board import Board
from textual.app import App


class Solitaire(App):
    """BINDINGS = {("r", "reset_game", "Reset Game")}
    CSS_PATH = "src/board.tcss"
    def on_mount(self):
        self.screen.styles.background = "green"
        self.mount(Board(id="board"))

    def action_reset_game(self):
        board = self.query_one("#board")
        Board.reset_game(board)"""
    
    def on_mount(self):
        self.screen.styles.background = "green"
        self.'''

def run():
    app = SolitaireApp()
    app.run()

if __name__ == "__main__":
    run()