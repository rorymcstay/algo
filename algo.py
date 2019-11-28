from src.marketdata import BUY, SELL
from src.marketdata import MarketData, TradeData, Quote
from src.publisher import Publisher, FileEngine, EventConfig
import logging

logging.basicConfig(level=logging.INFO)


def lobster_market_data_mapping(event, quote, *args):
    return event(
        symbol = "AAPL",
        nlevels=5,
        *[quote(args[i], args[i + 1], BUY if i+1 % 2 == 0 else SELL) for i in range(0,5,2)])


trades = EventConfig(dataClass=TradeData,
                     priority=2,
                     mapping=lambda *args: args)

marketdata = EventConfig(dataClass=MarketData,
                         priority=1,
                         mapping=lambda *args: lobster_market_data_mapping(MarketData, Quote, *args))

trades = Publisher("lobster_sample/AAPL_2012-06-21_34200000_37800000_message_30.csv", FileEngine, trades)
book = Publisher("lobster_sample/AAPL_2012-06-21_34200000_37800000_orderbook_30.csv", FileEngine, marketdata)

if __name__ == "__main__":
    trades.do()
