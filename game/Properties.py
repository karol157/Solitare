class Properties:
    """Represents the properties of a card in the game.

    Attributes:
        card_type (str): The type/category of the card (e.g., 'G', 'D', 'S', 'ST', 'STS').
        is_full (bool): Indicates if the card is fully visible or shown.
        is_visible (bool): Indicates if the card is visible at all.
        clickable (bool): Indicates if the card can be interacted with (clicked).
        order (str): Additional order information (e.g., 'F' for first).
        basic (bool): Marks if the card is considered a 'basic' card based on type and order.
    """

    def __init__(
        self,
        card_type: str = "g",
        is_full: bool = True,
        is_visible: bool = True,
        order: str = "",
    ):
        """
        Initialize Properties with card attributes.

        Args:
            card_type (str): Card type code, default is 'g' (general?).
            is_full (bool): Whether the card is fully shown, default True.
            is_visible (bool): Whether the card is visible, default True.
            order (str): Order flag, usually related to card placement or status.
        """
        self.card_type = card_type.upper()
        self.is_full = is_full
        self.is_visible = is_visible
        self.clickable = True
        self.order = order.upper()
        self.basic = False

        # Set clickable flag: only cards with type 'G' are clickable
        if self.card_type != "G":
            self.clickable = False
        
        # Determine if the card is basic based on type and order
        if self.card_type == "D" and self.order == "F":  # 'D' = Deck, 'F' = First
            self.basic = True
        elif self.card_type == "S":
            self.basic = True
        elif self.card_type in ("ST", "STS"):
            if order == "f":  # Lowercase 'f' here means basic for these types
                self.basic = True
