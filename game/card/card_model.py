from game.Properties import Properties


class CardModel:
    def __init__(self, figure: str, suit: str, properties: Properties):
        self.figure = figure.upper()
        self.suit = suit
        self.properties = properties
