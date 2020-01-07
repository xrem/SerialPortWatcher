#!/usr/bin/python
from subprocess import Popen
import sys
import time

filename = sys.argv[1]
while True:
    p = Popen(filename, shell=True)
    p.wait()
    print('Waiting 10 sec..')
    time.sleep(10)