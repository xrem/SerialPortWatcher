from .AbstractParser import AbstractParser

class FromFreezerParser(AbstractParser):

    def __init__(self):
        pass

    def parse(self, buf: bytes) -> str:
        if buf == b'EF010000EC':
            return 'Выберите товар'
        elif buf[0:8] == b'6D330064':
            return 'Поднесите карту к терминалу'
        elif buf[0:8] == b'00050035':
            return 'Что-то долго'
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
        else:
            return '<Unknown sequence>: ' + str(buf)
