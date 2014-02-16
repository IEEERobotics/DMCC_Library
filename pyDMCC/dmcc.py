"""Manage DMCC motors at a high level."""

import lib
from motor import Motor
from i2c_device import I2CDevice

BASE_ADDR = 0x2c
CAPE_ID = 'DMCC Mk.06'

def autodetect():
    """Probe to find all connected DMCCs.
    
    By setting the verify flag, the I2C address associated with each possible
    BBB cape is probed at a relevant register.  Those that respond accordingly
    will be added to the dictionary.

    """
    capes = {}
    for i in range(4):
        try:
            cape = DMCC(i, verify=True)
        except (RuntimeError, IOError) as e:
            continue
        capes[i] = cape
    return capes

class DMCC(object):

    """A single DMCC at a particular I2C address.  
    
    Each cape has two motors objects.

    """

    def __init__(self, id, verify=True):
        """Build logger, initial setup."""
        self.logger = lib.get_logger()

        if not (0 <= id <= 3) and not (BASE_ADDR <= id <= BASE_ADDR+3):
            err_msg = ("DMCC id can either be an index (0-3) " +
                "or an address ({}-{})".format(BASE_ADDR, BASE_ADDR+3))
            self.logger.error(err_msg)
            raise ValueError(err_msg)

        if (id <= 3):
            self.cape_num = id
        else:
            self.cape_num = id - BASE_ADDR

        self.i2c = I2CDevice(bus=1, address=self.address, config='dmcc_i2c.yaml')

        if verify:
            cape_str = self.i2c.registers['CapeId'].read()
            if cape_str[0:len(CAPE_ID)] != CAPE_ID:
                msg = "CapeId for device at {:#04x} is invalid: '{}'".format(
                            self.address, cape_str)
                self.logger.warning(msg)
                raise RuntimeError(msg)

        self.motors = {}
        for i in [1,2]:
            self.motors[i] = Motor(self.i2c, i)

        self.logger.debug("DMCC {}@{} initialized".format(
            self.cape_num, self.address))

    @property
    def address(self):
        return BASE_ADDR + self.cape_num

    @property
    def voltage(self):
        millivolts = self.i2c.registers['Voltage'].read()
        return millivolts/1000.0

