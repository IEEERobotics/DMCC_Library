"""Abstraction of a DMCC motor."""

import lib.lib as lib


class Motor(object):

    """Abstracts a hardware motor controlled by DMCC."""

    def __init__(self, board_num, motor_num):
        """Initializer for a motor object

        TODO: Actually setup the board and motor.

        :param board_num: Number of board that motor is controlled by (0 to 3).
        :type board_num: int
        :param motor_num: Number of motor to set velocity (1 or 2).
        :type motor_num: init
        :raises: ValueError

        """
        self.logger = lib.get_logger()

        if board_num < 0 or board_num > 3:
            err_msg = "Board number invalid (0-3): {}".format(board_num)
            self.logger.error(err_msg)
            raise ValueError(err_msg)

        if motor_num < 1 or motor_num > 2:
            err_msg = "Motor number invalid (1-2): {}".format(motor_num)
            self.logger.error(err_msg)
            raise ValueError(err_msg)

        self.board_num = board_num
        self.motor_num = motor_num
        self._velocity = 0

    def __str__(self):
        """Build human-readable representation of motor.

        :returns: String that describes this motor in a human-readable way.

        """
        return "board_num: {}, motor_num: {}".format(self.board_num,
            self.motor_num)

    @property
    def velocity(self):
        """Getter for motor's velocity."""
        return self._velocity

    @velocity.setter
    def velocity(self, velocity):
        """Set this motor to the given PID-controlled velocity.

        TODO: Take velocity as % of max, then convert.
        TODO: Actually speak I2C.

        :param velocity: Velocity to set motor to (-32768 to 32767).
        :type velocity: int

        """
        if velocity < -32768 or velocity > 32767:
            self.logger.warning("Velocity invalid (-32768-32767): {}".format(
                velocity))
            return False

        self._velocity = velocity
        self.logger.debug("Velocity set to {}".format(self._velocity))
