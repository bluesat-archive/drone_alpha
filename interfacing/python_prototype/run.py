#!/usr/bin/env python3
#
# Base code written by Tobias Brink - 2017
# Modified by Henry Veng for BLUESat Drone - April 2019
# Sauce: http://tbrink.science/blog/2017/04/30/processing-the-output-of-a-subprocess-with-python-in-realtime/
# Realtime input: https://eli.thegreenplace.net/2017/interacting-with-a-long-running-child-process-in-python/
#
# Comments by Mr Brink:
#   To the extent possible under law, the author(s) have dedicated
#   all copyright and related and neighboring rights to this software
#   to the public domain worldwide. This software is distributed
#   without any warranty.
#
#   You should have received a copy of the CC0 Public Domain
#   Dedication along with this software. If not, see
#   <http://creativecommons.org/publicdomain/zero/1.0/>.
#

import errno
import os
import pty
import select
import signal
import subprocess
import shlex
import time

# Set signal handler for SIGINT.
signal.signal(signal.SIGINT, lambda s,f: print("received SIGINT") )

class OutStream:
    def __init__(self, fileno):
        self._fileno = fileno
        self._buffer = ""

    def read_lines(self):
        try:
            output = os.read(self._fileno, 1000).decode()
        except OSError as e:
            if e.errno != errno.EIO: raise
            output = ""
        lines = output.split("\n")
        lines[0] = self._buffer + lines[0] # prepend previous
                                           # non-finished line.
        if output:
            self._buffer = lines[-1]
            return lines[:-1], True
        else:
            self._buffer = ""
            if len(lines) == 1 and not lines[0]:
                # We did not have buffer left, so no output at all.
                lines = []
            return lines, False

    def fileno(self):
        return self._fileno

# Start the drone interfacing code and wait 25 seconds for setup to finish
args_linked = shlex.split("python basic_interfacer.py --connect 127.0.0.1:14550")
link = subprocess.Popen(args_linked, stdin=subprocess.PIPE, stdout=None, universal_newlines=True)
time.sleep(25)

# Start the command generator with psuedo terminal utilities
out_r, out_w = pty.openpty()
args = shlex.split("python3 square_flight_generator.py")
proc = subprocess.Popen(args, stdout=out_w)
os.close(out_w)

# Read output of command generator and feed it into the interfacing process
fds = {OutStream(out_r)}
while fds:
    # Call select(), anticipating interruption by signals.
    while True:
        try:
            rlist, _, _ = select.select(fds, [], [])
            break
        except InterruptedError:
            continue
    # Handle all file descriptors that are ready.
    for f in rlist:
        lines, readable = f.read_lines()
        for line in lines:
            #write command to interfacing process
            link.stdin.write(line + '\n')
            link.stdin.flush()
        if not readable:
            # This OutStream is finished.
            fds.remove(f)

proc.terminate()
while(link.poll() == None):
    time.sleep(0.1)
link.terminate()