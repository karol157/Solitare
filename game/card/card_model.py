from game.Properties import Properties
from dataclasses import dataclass

@dataclass
class CardModel:
    """Card model for representing a card's properties and figure.
    Attributes:
        figure (str): The figure of the card (e.g., 'A', '2', ..., 'K').
        suit (str): The suit of the card (e.g., '♥', '♦', '♠', '♣').
        properties (Properties): An instance of Properties containing card attributes.
    """
    figure: str
    suit: str
    properties: Properties

    def __post_init__(self):
        """Post-initialization to ensure figure is uppercase."""
        self.figure = self.figure.upper()
