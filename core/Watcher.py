if __name__ == "__main__":
    raise ImportError()

# HACK: This imports here just to allow access to the top-level directory of project.
import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))

from serial import Serial as SerialPort
from models.StartupArguments import StartupArguments
from common.SerialPortDefaultOpenOptions import options
from common.DateHelper import getCurrentDate
from core.parsers.ParserFactory import Factory as ParserFactory


def console_log(msg):
    print("[{}] {}".format(getCurrentDate(), msg))

class Watcher():
    @staticmethod
    def __openSerialPort__(port: str, verbose=False) -> SerialPort:
        serialPort = SerialPort(**options)
        serialPort.port = port
        try:
            serialPort.open()
            if verbose:
                print("Port {0} is opened".format(port))
        except Exception as e:
            print('Problem opening port ' + port)
            print(e)
            exit(-1)
        return serialPort

    @property
    def verbose(self) -> bool:
        return self.__startupArguments__.verbose

    @property
    def kind(self):
        return self.__startupArguments__.kind

    def log(self, msg):
        console_log("{}:{}".format(self.kind, msg))

    def __init__(self, args: StartupArguments):
        self.__startupArguments__ = args
        self.__input__ = self.__openSerialPort__(args.portFrom, args.verbose)
        self.__output__ = self.__openSerialPort__(args.portTo, args.verbose)
        self.__buffer__ = b''
        self.__sequenceEnding__ = False
        self.__parser__ = ParserFactory.createParser(args.kind)

    def __processMessage__(self):
        self.log(self.__parser__.parse(self.__buffer__))

    def mainloop(self):
        console_log('Watcher initialized!')
        while 1:
            received_byte = self.__input__.read(size=1)
            if received_byte == b'\x02':
                self.__buffer__ = b''
            elif received_byte == b'\x03':
                if self.__sequenceEnding__ and received_byte == b'\x03':
                    self.__processMessage__()
                    self.__sequenceEnding__ = False
                elif self.__sequenceEnding__ and not received_byte == b'\x03' and self.verbose:
                    console_log('Malformed message received')
                else: #if __sequenceEnding__ was not yet raised
                    self.__sequenceEnding__ = True
            else:
                self.__buffer__ += received_byte
            self.__output__.write(received_byte)
            self.__output__.flush()



