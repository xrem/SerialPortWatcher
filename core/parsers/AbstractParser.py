from abc import ABCMeta, abstractmethod

from core.parsers.MessageTypeEnum import MessageTypeEnum


class AbstractParser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self, buf: bytes) -> str:
        pass

    @abstractmethod
    def get_type(self, message: str) -> MessageTypeEnum:
        pass