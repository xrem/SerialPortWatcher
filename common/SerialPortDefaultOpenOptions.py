if __name__ == "__main__":
    raise ImportError()

from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE

options = dict(
    baudrate=9600,
    bytesize=EIGHTBITS,
    parity=PARITY_NONE,
    stopbits=STOPBITS_ONE,
    timeout=None,
    xonxoff=False,
    rtscts=False,
    write_timeout=None,
    dsrdtr=False,
    inter_byte_timeout=None
)