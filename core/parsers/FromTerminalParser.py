from .AbstractParser import AbstractParser
from .MessageTypeEnum import MessageTypeEnum


class FromTerminalParser(AbstractParser):
    __idle__ = 'Готов. Выберите товар.'
    __failed__ = 'Нет денег.'
    __success__ = 'Чек 3 Толстый 2'
    __wait__ = 'Поднесите карту'

    def __init__(self):
        pass

    def parse(self, buf: bytes) -> str:
        if buf == b'01000003':
            return self.__idle__
        elif buf[0:8] == b'A00D0001':
            return self.__wait__
        elif buf[0:8] == b'A0070002':
            return 'Оплата'
        elif buf[0:8] == b'A0990003':
            return 'Чек 1'
        elif buf[0:8] == b'A05A0103':
            return 'Чек 2 Толстый (?)'
        elif buf[0:8] == b'A08A0103':
            return 'ddddddddddddddd'
        elif buf[0:8] == b'A0070002':
            return 'eeeeeeeeeeeeeee'
        elif buf[0:8] == b'009F0000':
            return self.__success__
        elif buf[0:8] == b'009F009B':
            return self.__failed__
        elif buf[0:8] == b'A0050004':
            return 'Оплата. (Прилетает всегда)'
        elif buf[0:8] == b'00050000':
            return 'hhhhhhhhhhhhhhh'
        else:
            return '<Unknown sequence>'

    def get_type(self,  message: str) -> MessageTypeEnum:
        if message == self.__idle__:
            return MessageTypeEnum.Idle
        if message == self.__failed__:
            return MessageTypeEnum.Failed
        if message == self.__success__:
            return MessageTypeEnum.Success
        if message == self.__wait__:
            return MessageTypeEnum.WaitingCard
        if 'Unknown sequence' not in message:
            return MessageTypeEnum.Nop
        return MessageTypeEnum.Unknown
