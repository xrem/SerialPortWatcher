if __name__ == "__main__":
    raise ImportError()

import argparse
from models.InputPortKind import InputPortKind
from models.StartupArguments import StartupArguments

parser = argparse.ArgumentParser()
parser.add_argument("portFrom", type=str, help="Input COM port (i.e. /dev/ttyS0)")
parser.add_argument("portTo", type=str, help="Output COM port (i.e. /dev/ttyS1)")
parser.add_argument("kind", type=InputPortKind.argparse, choices=list(InputPortKind), help="Speficy kind of input port")
parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
parser.add_argument("-l", "--logging", action="store_true", help="Enable file logging")
args = parser.parse_args()

if (args.verbose):
    print("Output level: verbose")
if (args.logging):
    print("File logging: enabled")

startupArguments = StartupArguments(args)