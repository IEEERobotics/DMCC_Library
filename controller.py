"""Manage DMCC motors at a high level."""

import lib.lib as lib
import motor as motor_mod


class Controller(object):

    """Manage DMCC motors at a high level.

    I'm not currently convinced of the need for a controller abstraction. Going
    to keep it for now as I work through how this should be architected.

    """

    def __init__(self):
        """Build logger, initial setup."""
        self.logger = lib.get_logger()
        self.motors = []
        self.logger.debug("Controller built")

    def build_motor(self, board_num, motor_num):
        """Create a motor object.

        :param board_num: Number of board that motor is controlled by (0 to 3).
        :type board_num: int
        :param motor_num: Number of motor to build (1 or 2).
        :type motor_num: int
        :returns: A newly constructed motor object.

        """
        new_motor = motor_mod.Motor(board_num, motor_num)
        self.logger.info("New motor created: ".format(new_motor))
        self.motors.append(new_motor)
        return new_motor
