"""Functions for interacting with motors controlled by DMCC."""

import lib.lib as lib

# Build logger
logger = lib.get_logger()


def set_velocity(board_num, motor_num, velocity):
    """Set the given motor to the given PID-controlled velocity.

    :param board_num: Number of board that motor is controlled by (0 to 3).
    :type board_num: int
    :param motor_num: Number of motor to set velocity (1 or 2).
    :type motor_num: init
    :param velocity: Velocity to set motor to (-32768 to 32767).
    :type velocity: int

    """
    if board_num < 0 or board_num > 3:
        logger.warning("Board number invalid (0-3): {}".format(board_num))
        return False

    if motor_num < 1 or motor_num > 2:
        logger.warning("Motor number invalid (1-2): {}".format(motor_num))
        return False

    if velocity < -32768 or velocity > 32767:
        logger.warning("Velocity invalid (-32768-32767): {}".format(velocity))
        return False
