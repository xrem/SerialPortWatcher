if __name__ == "__main__":
    raise ImportError()

# HACK: This imports here just to allow access to the top-level directory of project.
import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))

from serial import Serial as SerialPort
from models.StartupArguments import StartupArguments
from common.SerialPortDefaultOpenOptions import options

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

    def __init__(self, args: StartupArguments):
        self.__startupArguments__ = args
        self.__input__ = self.__openSerialPort__(args.portFrom, args.verbose)
        self.__output__ = self.__openSerialPort__(args.portFrom, args.verbose)
        self.__buffer__ = b''

    def __processMessage__(self):
        print(self.__buffer__)

    def mainloop(self):
        print('Watcher initialized!')
        while 1:
            received_byte = self.__input__.read(size=1)
            if received_byte == b'\x02':
                self.__buffer__ = b''
            elif received_byte == b'\x03':
                self.__processMessage__()
            else:
                self.__buffer__ += received_byte
            self.__output__.write(received_byte)
            self.__output__.flush()



