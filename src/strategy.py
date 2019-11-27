from src.marketdata import EVENT_TYPE
import logging

class Strategy():

    subscriptions = {}

    def __init__(self, **params):
        self.params = params

    def subscribe(self, event_type :EVENT_TYPE, act: callable = None):
        logging.info(f'subscribed to {event_type.__name__}')
        self.subscriptions.update({type(event_type): act})

    def onPublishedEvent(event: EVENT_TYPE) -> None:
        if self.subscriptions.get(type(event)) is not None:
            self.subcriptions[type(event)](event)
        else:
            logging.debug(f'{self.__name__} is doing nothing on {event_type.__name__}')


class Test(Strategy):

    def printEvent(event: EVENT_TYPE):
        logging.info(event)

