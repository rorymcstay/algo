BUY=1
SELL=2


class EventType:
    pass

class Quote:

    def __init__(self, price, qty, side, level):
        self.price = price
        self.qty = qty
        self.side = BUY if side == 1 else SELL
        self.level = level

    def __str__(self):
        return f'{self.side} {self.qty}@{self.price}'


class TradeData(EventType):

    def __init__(self, time, order_type, order_id, direction, size, price):
        self.type = order_type
        self.order_id = order_id
        self.time = time
        self.direction = BUY if direction == 1 else SELL
        self.size = size
        self.price = price

    def __str__(self):
        return f'dir={self.direction} {self.size}@{self.price} type={self.type}'


class MarketData(EventType):

    def __init__(self, symbol, nlevels, quotes):
        self.nlevels = nlevels
        self.symbol = symbol
        self.quotes = quotes
        self.buys = list(filter(lambda quote: quote.side == BUY, self.quotes))
        self.sells = list(filter(lambda quote: quote.side == SELL, self.quotes))

    def bestAsk(self):
        return min(x.price for x in self.sells)

    def bestBid(self):
        max(x.price for x in self.buys)

    def __str__(self):
        return f'{self.symbol}: nlevels: {self.nlevels}: {self.quotes}'
