if __name__ == "__main__":
    raise ImportError()

from enum import IntEnum


class InputPortKind(IntEnum):
    Freezer = 1
    Terminal = 2

    def __str__(self):
        return self.name.title()

    def __repr__(self):
        return str(self)

    @staticmethod
    def argparse(s: str):
        try:
            return InputPortKind[s]
        except KeyError:
            return s