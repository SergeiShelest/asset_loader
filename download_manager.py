import requests
import uuid
import os
from abc import ABCMeta, abstractmethod
from enum import Enum, auto
from dataclasses import dataclass, field


class NotifyType(Enum):
    NEW = auto()
    UPDATE = auto()
    COMPLETE = auto()


@dataclass
class File:
    title: str
    url: str
    path: str

    loaded: int = 0
    size: int = 0


@dataclass
class QueueFiles:
    title: str
    files: [File] = field(default_factory=list)
    uuid: str = ""

    def __post_init__(self):
        self.uuid = str(uuid.UUID(bytes=os.urandom(16), version=4))

    def add_file(self, file: File):
        self.files.append(file)


class IObserver:
    __metaclass__ = ABCMeta

    @abstractmethod
    def notify(self, type_: NotifyType, queue: QueueFiles):
        pass


class IObservable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def subscribe(self, subscriber: IObserver):
        pass

    @abstractmethod
    def unsubscribe(self, subscriber: IObserver):
        pass

    @abstractmethod
    def __notify_all(self, type_: NotifyType, queue: QueueFiles):
        pass


class HttpError(Exception):
    pass


class DownloadManager(IObservable):
    def __init__(self):
        self.__subscribers: [IObserver] = []

    def subscribe(self, subscriber: IObserver):
        self.__subscribers.append(subscriber)

    def unsubscribe(self, subscriber: IObserver):
        self.__subscribers.remove(subscriber)

    def __notify_all(self, type_, queue):
        for subscriber in self.__subscribers:
            subscriber.notify(type_, queue)

    def download(self, queue: [QueueFiles]):
        self.__notify_all(NotifyType.NEW, queue)

        for file in queue.files:
            r = requests.get(file.url, stream=True)

            if r.status_code != 200:
                raise HttpError("HTTP status {0}".format(r.status_code))

            file.size = int(r.headers.get('content-length'))

            with open(file.path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
                    file.loaded += len(chunk)

                    self.__notify_all(NotifyType.UPDATE, queue)

                self.__notify_all(NotifyType.COMPLETE, queue)
