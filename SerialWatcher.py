#!/usr/bin/python3

if __name__ != "__main__":
    raise ImportError("Usage: python ./SerialWatcher.py -h")

from common.DateHelper import getCurrentDate
# AutoExecutable:
from common.StartupArgumentParsing import startupArguments as args
from core.Watcher import Watcher

print("Startup: {}".format(getCurrentDate()))
print("[{0}] [{1}]-->[{2}] Initializing...".format(
    str(args.kind).title(),
    args.portFrom,
    args.portTo)
)

watcher = Watcher(args)
watcher.mainloop()