import csv
import logging
import threading
from threading import Thread
from multiprocessing import Process

from event_config import subscribers
from src.engine import ThreadPool

class EventConfig:

    def __init__(self, dataClass, mapping, complex=False):
        """
        The configuration class for an event to be published

        :param dataClass: the type of the data published
        :param complex: whether or not the mapping is complex TODO check the type of the result of the mapping instead
        :param mapping: the mapping to use. Either complex and returns the object or a tuple order mapping
        """

        self.dataClass = dataClass
        self.dataClass.mapping = mapping
        self.dataClass = dataClass
        self.complex = complex


class Engine:
    engine = None

    def __init__(self, connectionString):
        """
        Base class of Engines to provide to publisher

        :param connectionString: A single connection string to the feed
        """
        self.connectionString = connectionString
        pass

    def __iter__(self):
        pass


class FileEngine:

    def __init__(self, connectionString):
        """
        Stream over a file
        :param connectionString: path to file
        """
        self.engine = csv.reader(open(connectionString, 'r'))

    def __iter__(self):
        """
        The cursor to the data feed
        :return:
        """
        for line in self.engine:
            logging.debug(line)
            yield line


class Publisher(Process):

    def __init__(self, connectionString, engine, eventConfig):
        """
        Publish event to all subscribers in the global subscriber

        :param engine: the class of engine to use
        :param connectionString: parameter to engine
        :param eventConfig: the event config object
        """
        self.pause_cond = threading.Condition(threading.Lock())
        self.engine = engine(connectionString)
        self.data_type = eventConfig.dataClass
        self.complex = eventConfig.complex
        self.threadPool = ThreadPool(2)
        self.connectionString = connectionString

    def notifySubscribers(self, data):
        """
        Call back to global subscriber list

        :param data:
        :return:
        """
        global subscribers
        for sub in subscribers:
            self.threadPool.add_task(sub.onPublishedEvent, data)
        self.threadPool.wait_completion()

    def factory(self, *fields):
        """
        Construct events to publish

        :param fields:
        :return:
        """
        if self.complex:
            return self.data_type.mapping(*fields)
        else:
            return self.data_type(*self.data_type.mapping(*fields))

    def run(self) -> None:
        """
        Run method for the publisher

        :return:
        """
        logging.info(f'starting publisher {self.__class__} on {self.connectionString}')
        for i in self.engine:
            with self.pause_cond:
                logging.info(f'received {self.data_type.__name__} event: {i} ')
                self.notifySubscribers(self.factory(*i))
                self.pause_cond.wait(0.1)


    def init(self) -> None:
        """
        start the publisher in a new thread
        """
        Process.__init__(self, target=self.run, args=())
        self.name = self.connectionString
        self.start()
