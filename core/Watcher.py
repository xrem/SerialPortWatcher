if __name__ == "__main__":
    raise ImportError()

# HACK: This imports here just to allow access to the top-level directory of project.
import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))

import asyncio
import threading
from queue import SimpleQueue as Queue, Empty as EmptyQueueException
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
    def kind(self) -> str:
        return str(self.__startupArguments__.kind)

    def log(self, msg):
        console_log("{}:{}".format(self.kind, msg))

    def __init__(self, args: StartupArguments):
        self.__startupArguments__ = args
        self.__msgQueue__ = Queue()
        self.__input__ = self.__openSerialPort__(args.portFrom, args.verbose)
        self.__output__ = self.__openSerialPort__(args.portTo, args.verbose)
        self.__buffer__ = b''
        self.__sequenceEnding__ = False
        self.__parser__ = ParserFactory.createParser(args.kind)

    def __enqueueMessage__(self):
        self.__msgQueue__.put_nowait(self.__buffer__)

    async def __queueWatchCoro__(self) -> str:
        message = "No data"
        try:
            buffer = self.__msgQueue__.get(timeout=10)
            message = self.__parser__.parse(buffer)
        except EmptyQueueException:
            self.log('EmptyQueueException Raised')
        finally:
            return message

    async def __queueWatchTask__(self):
        while 1:
            task = asyncio.ensure_future(self.__queueWatchCoro__())
            result: str = await task
            if self.verbose:
                self.log(str)

    def __queueWatchWorker__(self):
        loop = asyncio.new_event_loop()
        asyncio.ensure_future(self.__queueWatchTask__(), loop=loop)
        self.log('Queue Watch Task is running')
        loop.run_forever()

    def mainloop(self):
        self.log('Watcher initialized!')
        queueWatcherThread = threading.Thread(target=self.__queueWatchWorker__)
        queueWatcherThread.start()

        while 1:
            received_byte = self.__input__.read(size=1)
            if received_byte == b'\x02':
                self.__buffer__ = b''
            elif received_byte == b'\x03':
                if self.__sequenceEnding__ and received_byte == b'\x03':
                    self.__enqueueMessage__()
                    self.__sequenceEnding__ = False
                elif self.__sequenceEnding__ and not received_byte == b'\x03' and self.verbose:
                    self.log('Malformed message received')
                else: #if __sequenceEnding__ was not yet raised
                    self.__sequenceEnding__ = True
            else:
                self.__buffer__ += received_byte
            self.__output__.write(received_byte)
            self.__output__.flush()



