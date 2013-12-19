"""Test cases for motor module."""

import unittest

import motor as motor_mod


class TestCreation(unittest.TestCase):

    """Test building DMCC motors."""

    def test_valid(self):
        """Test building a motor with valid board/motor numbers."""
        # Test min valid values
        new_motor = motor_mod.Motor(0, 1)
        assert type(new_motor) is motor_mod.Motor

        # Test max valid values
        new_motor = motor_mod.Motor(3, 2)
        assert type(new_motor) is motor_mod.Motor

    def test_invalid_board_num(self):
        """Test proper failure for invalid board numbers."""
        # Test board num below min value
        with self.assertRaises(ValueError):
            motor_mod.Motor(-1, 1)

        # Change motor num and assert same result
        with self.assertRaises(ValueError):
            motor_mod.Motor(-1, 2)

        # Test board num above max value
        with self.assertRaises(ValueError):
            motor_mod.Motor(4, 2)

        # Change motor num and assert same result
        with self.assertRaises(ValueError):
            motor_mod.Motor(4, 1)

    def test_invalid_motor_num(self):
        """Test proper failure for invalid motor numbers."""
        # Test motor num below min value
        with self.assertRaises(ValueError):
            motor_mod.Motor(0, 0)

        # Change board num and assert same result
        with self.assertRaises(ValueError):
            motor_mod.Motor(3, 0)

        # Test motor num above max value
        with self.assertRaises(ValueError):
            motor_mod.Motor(3, 3)

        # Change board num and assert same result
        with self.assertRaises(ValueError):
            motor_mod.Motor(0, 3)


class TestVelocity(unittest.TestCase):

    """Test motor velocity values."""

    def setUp(self):
        """Build DMCC motor abstraction."""
        self.motor = motor_mod.Motor(0, 1)

    def test_valid_series(self):
        """Test a series of valid velocities."""
        for vel in range(-32767, 32767, 1000):
            self.motor.velocity = vel
            assert self.motor.velocity == vel, "{} != {}".format(
                self.motor.velocity, vel)

    def test_invalid(self):
        """Test setting a motor to invalid velocities."""
        # Test velocity below min
        self.motor.velocity = -32769
        assert self.motor.velocity != -32769

        # Test velocity above max
        self.motor.velocity = 32768
        assert self.motor.velocity != 32768
