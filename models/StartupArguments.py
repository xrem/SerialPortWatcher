if __name__ == "__main__":
    raise ImportError()

from .InputPortKind import InputPortKind

class StartupArguments():
    def __init__(self, args):
        self.__portFrom__ = args.portFrom
        self.__portTo__ = args.portTo
        self.__kind__ = args.kind
        self.__verbose__ = args.verbose
        self.__logging__ = args.logging

    @property
    def portFrom(self) -> str:
        return self.__portFrom__

    @property
    def portTo(self) -> str:
        return self.__portTo__

    @property
    def kind(self) -> InputPortKind:
        return self.__kind__

    @property
    def verbose(self) -> bool:
        return self.__verbose__

    @property
    def logging(self) -> bool:
        return self.__logging__

