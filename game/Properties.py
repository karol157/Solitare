class Properties:
    def __init__(self, card_type: str='g', is_full: bool=True, is_visible: bool= True, order: str=''):
        self.card_type = card_type.upper()
        self.is_full = is_full
        self.is_visible = is_visible
        self.clickable = True
        self.order = order.upper()
        self.basic = False

        if self.card_type != 'G':
            self.clickable = False
        if self.card_type == 'D' and self.order == 'F':  # f -> first  d -> Deck
            self.basic = True
        elif self.card_type == 'S':
            self.basic = True
        elif self.card_type == 'ST' or self.card_type == 'STS':
            if order == 'f':
                self.basic = True