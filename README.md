#pyDMCC

Native Python library to control the Dual Motor Controller Cape for the BeagleBone Black.

## Authors

This is a fork of Exadler Technologies' C library. Huge shout-out to [Sarah Tan], [Paul Tan] and maybe others for building the hardware and original software. This repo is by the NCSU IEEE Robotics Team, and is heavily inspired by the original code base.

## Open Hardware

All hardware is Open Source and can be found [here](https://github.com/Exadler/DualMotorControlCape) (schematics, PCB, Eagle files).

## Motivation for Fork

The original DMCC library is in C with Python bindings. As of [Exadler/DMCC_Library@1d40b3a], it had performance issues that we believe relate to it's need to open an I2C file descriptor at every call (see below). The IEEE Robotics Team also doesn't need much of the functionally provided by the C code base, but does require code that's easy for new team members to understand, is well documented and clearly tested.

```python
In [1]: import time

In [2]: import hardware.dmcc_motor as dm_mod              

In [3]: m01 = dm_mod.DMCCMotor(0, 1)

In [4]: m02 = dm_mod.DMCCMotor(0, 2)

In [5]: m11 = dm_mod.DMCCMotor(1, 1)

In [6]: m12 = dm_mod.DMCCMotor(1, 2)

In [7]: def move(speed, duration, front_left, front_right, back_left, back_right):
    m01.power = speed * front_left
    m02.power = speed * front_right
    m11.power = speed * back_left
    m12.power = speed * back_right
    time.sleep(duration)
    m01.power = 0
    m02.power = 0
    m11.power = 0
    m12.power = 0

In [8]: def timeit(func):                                                   
    start = time.time()
    func()
    elapsed = time.time() - start
    print "Time elapsed: {} s".format(elapsed)

In [9]: def move_zero():
    move(0, 0.01, 1, -1, 1, -1)  # set all motors to 0 power, wait 0.01 sec, turn them to 0 again

In [10]: timeit(move_zero)
Time elapsed: 3.22693610191 s

In [11]: timeit(move_zero)
Time elapsed: 3.22623682022 s

In [12]: timeit(move_zero)
Time elapsed: 3.22612094879 s
```

[Exadler/DMCC_Library@1d40b3a]: https://github.com/Exadler/DMCC_Library/commit/1d40b3a9403ba6d3012fb83977c6eef426d84849
[Sarah Tan]: https://github.com/sarahttan
[Paul Tan]: https://github.com/paulctan
