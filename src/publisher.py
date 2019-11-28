import csv
import logging
from event_config import subscribers

class EventConfig():

    def __init__(self, dataClass, priority, mapping):
        self.dataClass = dataClass
        self.dataClass.mapping = mapping
        self.priority = priority
        self.dataClass = dataClass


class FileEngine():

    def __init__(self, connectionString):
        self.csvfile = csv.reader(open(connectionString, 'r'))

    def __iter__(self):
        for line in self.csvfile:
            logging.debug(line)
            yield line


class Publisher:

    def __init__(self, connectionString, engine, eventConfig):
         self.engine = engine(connectionString)
         self.data_type = eventConfig.dataClass

    def notifySubscribers(self, data):
        global subscribers
        for sub in subscribers:
            sub.onPublishedEvent(data)

    def factory(self, *fields):
        return self.data_type(*self.data_type.mapping(*fields))

    def do(self):
        for i in self.engine:
            self.notifySubscribers(self.factory(*i))
