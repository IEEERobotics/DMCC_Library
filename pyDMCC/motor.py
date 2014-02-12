"""Abstraction of a DMCC motor."""

import lib.lib as lib

class Motor(object):

    """Abstracts a hardware motor controlled by DMCC."""

    def __init__(self, i2c_device, motor_num):
        """Initializer for a motor object

        TODO: Actually setup the board and motor.

        :param board_num: Number of board that motor is controlled by (0 to 3).
        :type board_num: int
        :param motor_num: Number of motor to set velocity (1 or 2).
        :type motor_num: init
        :raises: ValueError

        """
        self.logger = lib.get_logger()

        if not motor_num in [1,2]:
            err_msg = "Motor number invalid (1-2): {}".format(motor_num)
            self.logger.error(err_msg)
            raise ValueError(err_msg)

        self.motor_num = motor_num
        self.i2c = i2c_device
        self._velocity = 0

    def __str__(self):
        """Build human-readable representation of motor.

        :returns: String that describes this motor in a human-readable way.

        """
        return "DMCC motor {} at I2C addresss {:#4x}".format(
                self.motor_num, self.i2c.address)

    def refresh(self):
        self.i2c.registers['Execute'].write('Refresh')

    # TODO: change these to non-decorated properties so we can call the
    # getter/setters with params (such as skipping the execute/refresh)
    @property
    def power(self):
        """Getter for motor power.

        BBB execution time: ~2ms
        
        """
        self.refresh()
        reg = "PowerMotor" + str(self.motor_num)
        return self.i2c.registers[reg].read() / 100.0

    @power.setter
    def power(self, power):
        """Set this motor to the given power.

        For performance reasons, avoid calls slow class (e.g. Str.foramt{}
        within the realm of normal operation.

        BBB execution time: ~4ms

        :param power: Power to set motor to (-100 to 100).
        :type power: float

        """
        if not(-100 <= power <= 100):
            self.logger.warning(
                    "Power invalid (-100.0 to 100.0): {}".format(power))
            return False

        # DMCC actually clamps values within -10000 to +10000
        data_reg = "PowerMotor" + str(self.motor_num)
        self.i2c.registers[data_reg].write(int(power*100))

        control_id = "Set_Motor" + str(self.motor_num) + "_Power"
        self.i2c.registers['Execute'].write(control_id)
       
        self.logger.debug("Power set to %d", power)

    @property
    def position(self):
        """Return motor position.

        BBB execution time:
        
        """
        self.refresh()
        reg = "QEI" + str(self.motor_num) + "Position"
        return self.i2c.registers[reg].read()

    @property
    def velocity(self):
        """Return motor velocity.

        BBB execution time:
        
        """
        self.refresh()
        reg = "QEI" + str(self.motor_num) + "Velocity"
        return self.i2c.registers[reg].read()

