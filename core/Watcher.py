if __name__ == "__main__":
    raise ImportError()

# HACK: This imports here just to allow access to the top-level directory of project.
import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))

import asyncio
import threading
import socketio
from queue import SimpleQueue as Queue, Empty as EmptyQueueException
from serial import Serial as SerialPort
from models.StartupArguments import StartupArguments
from common.SerialPortDefaultOpenOptions import options
from common.DateHelper import getCurrentDate
from core.parsers.ParserFactory import Factory as ParserFactory
from core.SocketHubNsp import SocketHubNsp


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
        self.__sio__ = socketio.AsyncClient(reconnection=True)
        self.__nsp__ = '/'+self.kind
        self.__sio__.register_namespace(SocketHubNsp(self.__nsp__))
        self.__halt__ = False

    def __enqueueMessage__(self):
        self.__msgQueue__.put_nowait(self.__buffer__)

    async def __queueWatchCoro__(self) -> dict:
        message = "No data"
        buffer = b''
        try:
            buffer = self.__msgQueue__.get(timeout=10)
            message = self.__parser__.parse(buffer)
        except EmptyQueueException:
            self.log('EmptyQueueException Raised')
        finally:
            if 'Unknown sequence' in message:
                return {'status': message, 'buffer': str(buffer)}
            else:
                return {'status': message}


    async def __queueWatchTask__(self):
        while 1:
            task = asyncio.ensure_future(self.__queueWatchCoro__())
            data: dict = await task
            if self.verbose:
                self.log(data)
            if self.__sio__.connected:
                try:
                    await self.__sio__.emit('event', data=data, namespace=self.__nsp__)
                except Exception as e:
                    console_log('Emit error: ' + str(e))
                    self.__halt__ = True
            else:
                console_log('No connection to hub.')
                self.__halt__ = True


    async def __initializeSocketIOConnection__(self):
        try:
            await self.__sio__.connect('http://localhost:3000/', transports=['polling'])
        except Exception as e:
            console_log('Connection to hub failed: ' + str(e))
            self.__halt__ = True

    def __queueWatchWorker__(self):
        loop = asyncio.new_event_loop()
        asyncio.ensure_future(self.__queueWatchTask__(), loop=loop)
        self.log('Queue Watch Task is running')
        loop.run_forever()

    def __socketIOWorker__(self):
        loop = asyncio.new_event_loop()
        asyncio.ensure_future(self.__initializeSocketIOConnection__(), loop=loop)
        loop.run_forever()

    # noinspection PyUnreachableCode
    def mainloop(self):
        self.log('Initializing...')
        queueWatcherThread = threading.Thread(target=self.__queueWatchWorker__)
        queueWatcherThread.setDaemon(True)
        queueWatcherThread.start()
        socketIOThread = threading.Thread(target=self.__socketIOWorker__)
        socketIOThread.setDaemon(True)
        socketIOThread.start()

        # Await for connection in sync manner
        while not self.__sio__.connected and not self.__halt__:
            pass

        if self.__sio__.connected:
            self.log('Watcher initialized!')
        else:
            self.log("Failed. Rerunning...")
            sys.exit(-1)

        try:
            while not self.__halt__:
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
        except KeyboardInterrupt:
            self.log('Terminating...')

        self.log('Halt')
        sys.exit(-2)

        queueWatcherThread.join()
        socketIOThread.join()
