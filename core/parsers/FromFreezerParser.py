from .AbstractParser import AbstractParser
from .MessageTypeEnum import MessageTypeEnum


class FromFreezerParser(AbstractParser):
    __idle__ = 'Выберите товар'
    __extendedWait__ = 'Что-то долго'
    __refund__ = 'Refund'
    __wait__ = 'Поднесите карту к терминалу'

    def __init__(self):
        pass

    def parse(self, buf: bytes) -> str:
        if buf == b'EF010000EC':
            return self.__idle__
        elif buf[0:6] == b'6D3300' and buf[7:8] != b'00':
            return self.__wait__
        elif buf[0:8] == b'00050035':
            return self.__extendedWait__
        elif buf[0:8] == b'00050000':
            return 'Оплата'
        elif buf[0:8] == b'00050100':
            return 'Чек 1'
        elif buf[0:8] == b'007D0000':
            return 'Чек 2 Толстый'
        elif buf[0:8] == b'00960000':
            return 'Чек 2 Покороче'
        elif buf[0:8] == b'006D0000':
            return 'Чек 1 : нет денег'
        elif buf[0:8] == b'A0140003':
            return 'Завершено'
        elif len(buf) >= 20 and buf[0:20] == b'6D33000000000000000D':
            return self.__refund__
        else:
            return '<Unknown sequence>'

    def get_type(self,  message: str) -> MessageTypeEnum:
        if message == self.__idle__:
            return MessageTypeEnum.Idle
        if message == self.__extendedWait__:
            return MessageTypeEnum.ExtendedWait
        if message == self.__refund__:
            return MessageTypeEnum.Refund
        if message == self.__wait__:
            return MessageTypeEnum.WaitingCard
        if 'Unknown sequence' not in message:
            return MessageTypeEnum.Nop
        return MessageTypeEnum.Unknown