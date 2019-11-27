from src.publisher import EVENT_TYPE

BUY=1
SELL=2

class Quote:

    def __init__(self, price, qty, side, level, time):
        self.price = price
        self.qty = qty
        self.side = BUY if side == 1 else SELL
        self.level = level
        self.time = time

    def __str__(self):
        return f'{self.side} {self.qty}@{self.price}'

class TradeData(EVENT_TYPE):
    def __init__(self, time, order_type, order_id, symbol, direction, size, price):
        self.time = time
        self.symbol = symbol
        self.direction = BUY if side == 1 else SELL
        self.size = size
        self.price = price
    def __str__():
        return f'dir={self.direction} {self.size}@{self.price} type={self.type}'

class MarketData(EVENT_TYPE):

    def __init__(self, symbol, nlevels, *quotes):
        self.nlevels = nlevels
        self.symbol = symbol
        self.quotes = quotes
        self.buys = list(filter(lambda x: quote.side == BUY, self.quotes)).sort(key = lambda x: x.level)
        self.sells= list(filter(lambda x: quote.side == SELL, self.quotes)).sort(key = lambda x: x.level)

    def create(*fields):
        MarketData(EVENT_TYPE.mapping(*fields))

    def bestAsk(self):
        min(x.price for x in self.sells)

    def bestBid(self):
        max(x.price for x in self.buys)

    def __str__():
        return f'{self.symbol}: nlevels: {self.nlevels}: {self.quotes}'
