from src.marketdata import MarketData, TradeData
import logging

class Strategy():

    subscriptions = {}

    def __init__(self, **params):
        self.params = params

    def onPublishedEvent(self, event) -> None:
        type = event.__class__.__name__
        if self.subscriptions.get(type) is not None:
            self.subscriptions[type](event)
        else:
            logging.debug(f'{self.__class__.__name__} is doing nothing on {event.__name__}')

    @staticmethod
    def subscribed(event_type, subscriptions=subscriptions):

        def action(func):
            subscribed_event = event_type

            def wrapper(event, *args, **kwargs):
                if event is isinstance(event, type(subscribed_event)):
                    return func(*args, **kwargs)
            return wrapper
        subscriptions.update({event_type.__name__: action})
        return action


class Test(Strategy):

    @Strategy.subscribed(TradeData)
    def printEvent(self, event):
        print(event)
