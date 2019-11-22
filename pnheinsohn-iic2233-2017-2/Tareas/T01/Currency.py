class Currency:

    list_of_coins = []

    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name
        self._amount = 0
        self.list_of_coins.append(self)
        Currency.list_of_coins = self.list_of_coins

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if value < 0:
            self._amount = 0
        else:
            self._amount = value

    def __repr__(self):
        return self.symbol + ": " + str(self.amount)