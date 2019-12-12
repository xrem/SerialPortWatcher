if __name__ == "__main__":
    raise ImportError()

# HACK: This imports here just to allow access to the top-level directory of project.
import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))

import socketio
from common.DateHelper import getCurrentDate


def console_log(msg):
    print("[{}] {}".format(getCurrentDate(), msg))

class SocketHubNsp(socketio.AsyncClientNamespace):
    def on_connect(self):
        console_log("SocketIO: Connected")

    def on_disconnect(self):
        console_log("SocketIO: Disconnect")

    def on_connect_error(self, data):
        console_log("SocketIO: Connection error\n"+str(data))

    def on_connect_timeout(self):
        console_log("SocketIO: Connection timeout")

    def on_reconnect(self, data):
        console_log("SocketIO: Successful reconnection ("+str(data)+")")

    def on_reconnect_error(self, data):
        console_log("SocketIO: Reconnection error ("+str(data)+")")

    def on_reconnect_failed(self, data):
        console_log("SocketIO: Reconnection failed ("+str(data)+")")

    def on_reconnecting(self, data):
        console_log("SocketIO: Reconnecting... ("+str(data)+")")

