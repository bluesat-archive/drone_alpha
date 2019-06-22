#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Generates velocity vectors once every second to fly a square path
# Author: Henry Veng
# Written: April 2019

import time
import sys

for i in range(10):
    sys.stdout.write("1,0,0\n")
    time.sleep(1)

for i in range(10):
    sys.stdout.write("0,1,0\n")
    time.sleep(1)

for i in range(10):
    sys.stdout.write("-1,0,0\n")
    time.sleep(1)

for i in range(10):
    sys.stdout.write("[0,-1,0]\n")
    time.sleep(1)

for i in range(10):
    sys.stdout.write("0,-1,0\n")
    time.sleep(1)

sys.stdout.write("l")