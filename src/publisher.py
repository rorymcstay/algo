import csv
import logging

class EventConfig():
    def __init__(self,priority, mapping):
        self.mapping = mapping
        self.priority = priority

class EVENT_TYPE:
    def __init__(self, config: EventConfig):
        self.config = config
        self.mapping = mapping

class FileEngine():

    def __init__(self, connectionString):
        self.csvfile = csv.reader(open(connectionString, 'r'))

    def __iter__(self):
        for line in self.csvfile:
            logging.debug(line)
            yield line

class Publisher:

    subscriptions = {}
    def __init__(self, connectionString, engine, data_type: EVENT_TYPE):
         self.engine = engine(connectionString)
         self.data_type = data_type

    def notifySubscribers(self, data):
        return map(lambda sub: self.get(sub).onPublishedEvent(event_type=self.data_type), self.subscriptions)

    def onSubscription(self, name, strategy):
        self.subscription.update({name: strategy})
        strategy.subscribe(type(self.data_type))

    def do(self):
        for i in self.engine:
            self.notifySubscribers(i)
