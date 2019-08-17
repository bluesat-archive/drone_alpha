#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ultrasonic Collision Detection Script
Author: Takumi Iwasa, Henry Veng
Written: June 2019
Last modified: August 2019
"""

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class UltraSonic:
    def __init__(self, trigger_pin, echo_pin):
        self._trigger = trigger_pin
        self._echo = echo_pin
        GPIO.setup(self._trigger, GPIO.OUT)
        GPIO.setup(self._echo, GPIO.IN)

    def distance(self):
        GPIO.output(self._trigger, True)

        time.sleep(0.00001)
        GPIO.output(self._trigger, False)

        start_time = time.time()
        stop_time = time.time()

        while GPIO.input(self._echo) == 0:
            start_time = time.time()

        while GPIO.input(self._echo) == 1:
            stop_time = time.time()

        time_elapsed = stop_time - start_time

        distance = (time_elapsed * 34300) / 2

        return distance

from dronekit import connect, VehicleMode

vehicle = connect('udpin:127.0.0.1:14552', wait_ready=False)
vehicle.initialize(8, 30)
vehicle.wait_ready('autopilot_version')

def range_sensor(dist, orient):
    msg = vehicle.message_factory.distance_sensor_encode(
        0,
        2,
        400,
        dist,
        1,
        1,
        orient,
        0
    )

    print(msg)
    vehicle.send_mavlink(msg)

sensor0 = UltraSonic(18, 24)

while True:
    range_sensor(sensor0.distance, 0)
    time.sleep(0.02)

'''
if __debug__:
    sensor1 = UltraSonic(18, 24)
    try:
        while True:
            print("Measured Distance = %.1f cm" % sensor1.distance())
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
'''