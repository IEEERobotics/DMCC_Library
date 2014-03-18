#!/usr/bin/env python

import os, sys
from pprint import pprint
import pyDMCC

import signal
from time import time,sleep

def cleanup(signum, frame):
    print "Powering down..."
    for d in dmccs.values():
        for m in d.motors.values():
            m.power = 0
    exit(0)

signal.signal(signal.SIGINT, cleanup)

dmccs = pyDMCC.autodetect()

for d in dmccs.values():
    print "DMCC #{} @ {:#04x} : Voltage = {}".format(
            d.cape_num, d.address, d.voltage)

print
for d in dmccs.values():
    print "DMCC #{} @ {:#04x}:".format(d.cape_num, d.address)
    motor = d.motors[1]
    num = 100
    print "  {} reads in... ".format(num),
    start = time()
    for i in range(num):
        x = motor.position
    elapsed = time() - start
    print "{:0.3f} seconds ({:0.2f} ms each).".format(elapsed, 1000*elapsed/num)
    print "  {} sets in... ".format(num),
    start = time()
    for i in range(num):
        motor.power = 0
    elapsed = time() - start
    print "{:0.3f} seconds ({:0.2f} ms each).".format(elapsed, 1000*elapsed/num)


print
for d in dmccs.values():
    for m in d.motors.values():
        print m, ":"
        for power in [20,40,60,80,100,0,-20,-40,-60,-80,-100]:
            print "Setting power to {}%".format(power)
            m.power = power
            start = time()
            while time() - start < 1:
                print "  Pos: {:06} Vel: {:03} Cur: {} mA".format(
                        m.position, m.velocity, m.current)
                sleep(0.1)
        print "Setting power to 0%"
        m.power = 0
        print



