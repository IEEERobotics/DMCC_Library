"""Abstraction of a DMCC motor."""

import lib

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
        """Refresh the status registers for reading"""
        self.i2c.registers['Execute'].write('Refresh')

    def reset(self):
        """Reset QEI"""
        reg = "Clear_QEI" + str(self.motor_num)
        self.i2c.registers['Execute'].write(reg)

    # NOTE: Always zero?
    @property
    def status(self):
        """Getter for motor status bits.

        """
        self.refresh()
        reg = "Status"
        field = "ModeMotor" + str(self.motor_num)
        return self.i2c.registers[reg].read(field)

    @property
    def current(self):
        """Return motor current.

        """
        self.refresh()
        reg = "CurrentMotor" + str(self.motor_num)
        return self.i2c.registers[reg].read()

    # NOTE: Reading not implemented?
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

    @position.setter
    def position(self, position):
        """Set motor position (for PID).
        
        """
    
        reg = "TargetPosition" + str(self.motor_num)
        self.i2c.registers[reg].write(position)
        self.i2c.registers['Execute'].write('Set_Motor1_Position')

    @property
    def velocity(self):
        """Return motor velocity.

        BBB execution time:
        
        """
        self.refresh()
        reg = "QEI" + str(self.motor_num) + "Velocity"
        return self.i2c.registers[reg].read()

    @velocity.setter
    def velocity(self, velocity):
        """Return motor velocity (for PID).
        
        """
    
        reg = "TargetVelocity" + str(self.motor_num)
        self.i2c.registers[reg].write(velocity)
        self.i2c.registers['Execute'].write('Set_Motor1_Speed')


    """ PID methods """

    def _get_pid(self, mode):
        prefix = mode + str(self.motor_num)  
        params = [] 
        for name in  ['Kp', 'Ki', 'Kd']:
            reg = prefix + name
            params.append(self.i2c.registers[reg].read())
        return tuple(params)

    def _set_pid(self, mode, params):
        for p in params:
            if not (-32768 <= p <= 32767):
                err_msg = "PID params must be [-32768,+32767]: {}".format(params)
                self.logger.error(err_msg)
                raise ValueError(err_msg)
        params = list(params)
        prefix = mode + str(self.motor_num)  
        for name in  ['Kp', 'Ki', 'Kd']:
            reg = prefix + name
            k = params.pop(0)
            self.i2c.registers[reg].write(k)

    @property
    def position_pid(self):
        return self._get_pid('Pos')

    # NOTE: Would be nice if there was a way to set maximum velocity or power
    # for this
    @position_pid.setter
    def position_pid(self, params):
        return self._set_pid('Pos', params)

    @property
    def velocity_pid(self):
        return self._get_pid('Vel')

    @velocity_pid.setter
    def velocity_pid(self, params):
        return self._set_pid('Vel', params)
    # NOTE: Not implemented?
    @property
    def pid_error(self):
        """Return error from PID calculations

        """
        self.refresh()
        reg = "PID" + str(self.motor_num) + "Error"
        return self.i2c.registers[reg].read()

