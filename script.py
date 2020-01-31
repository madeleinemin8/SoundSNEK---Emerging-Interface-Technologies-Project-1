import time
import os

mtime_last = 0
dir = os.path.dirname(os.path.realpath(__file__))+"/test"
while True:
    mtime_cur = os.path.getmtime(dir)
    if mtime_cur != mtime_last:
        with open(dir, 'r') as f:
            print(f.read())
    mtime_last = mtime_cur
