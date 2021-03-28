import logging
from src.marketdata import BUY, SELL
from src.marketdata import MarketData, TradeData, Quote
from src.publisher import Publisher, FileEngine, EventConfig

logging.basicConfig(level=logging.INFO)


def lobster_market_data_mapping(event, quote, *args):
    quotes = [quote(price=args[i],
                    qty=args[i + 1],
                    side=BUY if i+1 % 2 == 0 else SELL,
                    level=1) for i in range(0, 120, 2)]
    return event(symbol="AAPL", nlevels=30, quotes=quotes)


trades = EventConfig(dataClass=TradeData,
                     mapping=lambda *args: args)

marketdata = EventConfig(dataClass=MarketData,
                         mapping=lambda *args: lobster_market_data_mapping(MarketData, Quote, *args),
                         complex=True)

trades = Publisher("lobster_sample/AAPL_2012-06-21_34200000_37800000_message_30.csv",
                   engine=FileEngine,
                   eventConfig=trades)

marketdata = Publisher(connectionString="lobster_sample/AAPL_2012-06-21_34200000_37800000_orderbook_30.csv",
                       engine=FileEngine,
                       eventConfig=marketdata)


if __name__ == "__main__":
    for publisher in [trades, marketdata]:
        publisher.init()
