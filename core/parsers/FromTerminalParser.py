from .AbstractParser import AbstractParser

class FromTerminalParser(AbstractParser):

    def __init__(self):
        pass

    def parse(self, buf: bytes) -> str:
        if buf == b'01000003':
            return 'Готов. Выберите товар.'
        elif buf[0:8] == b'A00D0001':
            return 'Поднесите карту'
        elif buf[0:8] == b'A0070002':
            return 'Оплата'
        elif buf[0:8] == b'A0990003':
            return 'Чек 1'
        elif buf[0:8] == b'A05A0103':
            return 'Чек 2 Толстый (приходит когда нет денег)'
        elif buf[0:8] == b'A08A0103':
            return 'ddddddddddddddd'
        elif buf[0:8] == b'A0070002':
            return 'eeeeeeeeeeeeeee'
        elif buf[0:8] == b'009F0000':
            return 'Чек 3 Толстрый 2'
        elif buf[0:8] == b'009F009B':
            return 'Нет денег.'
        elif buf[0:8] == b'A0050004':
            return 'Оплата. (Прилетает всегда)'
        elif buf[0:8] == b'00050000':
            return 'hhhhhhhhhhhhhhh'
        else:
            return '<Unknown sequence>: ' + str(buf)
