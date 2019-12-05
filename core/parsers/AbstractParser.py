from abc import ABCMeta, abstractmethod


class AbstractParser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self, buf: bytes) -> str:
        pass