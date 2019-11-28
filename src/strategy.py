from src.marketdata import MarketData, TradeData
import logging

class Strategy(object):

    def __init__(self, **params):
        """
        Inherit this class and annotate methods with Strategy.subscribe(EventType) to act on the
        publishing of an event.

        Methods to act on a strategy must take only a single parameter at this time.

        A method may only subscribe to one event at this time.

        :param params:
        """
        self.params = params

    def _postOrder(self):
        pass

    def onPublishedEvent(self, *args, **kwargs) -> None:
        """
        call methods registered to a specific event

        :param args:
        :param kwargs:
        :return:
        """
        public_method_names = [method for method in dir(self) if callable(getattr(self, method)) if not method.startswith('_')]
        for method in public_method_names:
            if method == "onPublishedEvent":
                continue

            getattr(self, method)(*args, **kwargs)

    @staticmethod
    def subscribed(event_type):
        """
        Annotation to register a class method to the publishing of an event type

        :param event_type: An event type defined
        :return:
        """

        def action(func):
            def wrapper(*args, **kwargs):
                if isinstance(args[1], event_type):
                    func(*args, **kwargs)
                else:
                    logging.debug(f'not doing anthing {event_type}')
            return wrapper

        return action


class Test(Strategy):

    @Strategy.subscribed(TradeData)
    def printTradeEvent(self, event):
        print(f'trade event {event}')

    @Strategy.subscribed(MarketData)
    def printMarketData(self, event: MarketData):
        print(event.bestAsk())
