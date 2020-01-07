if __name__ == "__main__":
    raise ImportError()

from enum import IntEnum


class MessageTypeEnum(IntEnum):
    Unknown = 0
    Success = 1
    Failed = 2
    Idle = 3
    Refund = 4
    Nop = 5
    ExtendedWait = 6