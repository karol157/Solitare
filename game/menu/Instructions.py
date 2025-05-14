from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Static, Header, Footer

class InstructionsScreen(Screen):
    """Displays game instructions."""
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back to Menu", show=True)
    ]

    def compose(self) -> ComposeResult:
        yield Header(name="How to Play")
        with Container(classes="content-screen-container"): # Use the new container
            with ScrollableContainer(classes="content-box"):
                yield Static("--- HOW TO PLAY SOLITAIRE ---", classes="content-title")
                yield Static(
                    """
Goal:  
Move all cards to the four foundation piles — one for each suit — in ascending order (Ace to King).  
                    
Gameplay:  
    - Tableau: Build columns in descending order, alternating colors.  
    - Stock: Deal cards from the stock pile to the waste pile.  
    - Waste: The top card can be moved to the tableau or foundation.  
    - Foundation: Build each pile by suit, from Ace to King.  
                    
Keys:  
    - 'R' → Reset the game  
    - 'Escape' → Return to game / Quit game  
                    """,
                    classes="content-text"
                )
                with Vertical(classes="button-container-centered"):
                    yield Button("Back to Menu", id="back_to_menu", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back_to_menu":
            self.app.pop_screen()