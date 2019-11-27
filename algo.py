from src.marketdata import BUY, SELL
from src.strategy import Strategy, Test
from src.marketdata import MarketData, TradeData
from src.publisher import Publisher, FileEngine, EventConfig

import logging

logging.basicConfig(level = logging.INFO)

def lobster_market_data_mapping(event, quote, *args):
    return event(
        symbol = "AAPL",
        nlevels=5,
        *[quote(args[i], args[i + 1], BUY if i+1 % 2 == 0 else SELL) for i in range(0,5,2)])

events = {
    "lobster_book_data": EventConfig(priority = 1,
                                     mapping = lambda args: lobster_maret_data_mapping(MarketData,
                                                                Quote, args)),
    "lobster_trade_data": EventConfig(priority = 2,
                                      mapping = lambda args: TradeData(*args))
         }



trades = Publisher("lobster_sample/AAPL_2012-06-21_34200000_37800000_message_30.csv", FileEngine, TradeData)
book = Publisher("lobster_sample/AAPL_2012-06-21_34200000_37800000_orderbook_30.csv", FileEngine, MarketData)
if __name__ == "__main__":
   strat = Test()
   strat.subscribe(MarketData, "lobster_book_data")
   strat.subscribe(TradeData, "lobster_trade_data")
   trades.do()



