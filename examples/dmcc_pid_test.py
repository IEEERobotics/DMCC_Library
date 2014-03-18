#!/usr/bin/env python

import os, sys
import pyDMCC

import signal
from time import time,sleep

def cleanup(signum, frame):
    print "Powering down... ",
    for d in dmccs.values():
        for m in d.motors.values():
            m.power = 0
    print "done."
    exit(0)

signal.signal(signal.SIGINT, cleanup)

def status():
    print "  S:{}, Pos: {:+07}, Vel: {:+04}, Err: {:d}, Pow: {:05.1f}, Cur: {} mA".format(
            motor.status, motor.position, motor.velocity, motor.pid_error, motor.power, motor.current)


dmccs = pyDMCC.autodetect()

for d in dmccs.values():
    print "DMCC #{} @ {:#04x} : Voltage = {}".format(
            d.cape_num, d.address, d.voltage)

motor = dmccs[0].motors[1]

print "PID constants (pos):", motor.position_pid
constants =  (-5000, -200, -500)
print "Setting to: ", str(constants)
motor.position_pid = constants
print "PID constants (pos):", motor.position_pid

motor.reset()
goal = 5000
print "Setting position target to {}...".format(goal)
motor.position = goal
start = time()
while abs(motor.position -goal) > 10:
    status()
    sleep(0.1)
print

print "PID constants (vel):", motor.velocity_pid
constants =  (-3000, -32768, 0)
print "Setting to: ", str(constants)
motor.velocity_pid = constants
print "PID constants (vel):", motor.velocity_pid

goal = 150
print "Setting velocty target to {}...".format(goal)
motor.velocity = goal
start = time()
while abs(motor.velocity - goal) > 5:
    status()
    sleep(1)

cleanup(0,0)
