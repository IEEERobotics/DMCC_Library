"""Test cases for controller module."""

import unittest

import controller as controller_mod
import motor as motor_mod


class TestBuildMotor(unittest.TestCase):

    """Test building DMCC motors."""

    def setUp(self):
        """Build controller."""
        self.controller = controller_mod.Controller()

    def test_type(self):
        """Confirm return type is motor.Motor"""
        new_motor = self.controller.build_motor(0, 1)
        assert type(new_motor) is motor_mod.Motor

    def test_invalid(self):
        """Test proper failure for invalid board/motor numbers."""
        with self.assertRaises(ValueError):
            self.controller.build_motor(-1, -1)
