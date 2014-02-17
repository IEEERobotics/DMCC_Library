"""Test cases for motor module."""

import unittest

from pyDMCC.motor import Motor, lib
from os import path

class TestCreation(unittest.TestCase):

    """Test building DMCC motors."""

    def setUp(self):
        config = path.dirname(path.realpath(__file__))+"/test_config.json"
        lib.get_config(config)

    def test_valid(self):
        """Test building a motor with valid board/motor numbers."""
        # Test min valid values
        new_motor = Motor(0, 1)
        assert type(new_motor) is Motor

        # Test max valid values
        new_motor = Motor(3, 2)
        assert type(new_motor) is Motor

    def test_invalid_motor_num(self):
        """Test proper failure for invalid motor numbers."""
        # Test motor num below min value
        with self.assertRaises(ValueError):
            Motor(0, 0)

        # Change board num and assert same result
        with self.assertRaises(ValueError):
            Motor(3, 0)

        # Test motor num above max value
        with self.assertRaises(ValueError):
            Motor(3, 3)

        # Change board num and assert same result
        with self.assertRaises(ValueError):
            Motor(0, 3)


