"""Test cases for controller module."""

import unittest

from pyDMCC.dmcc import DMCC, Motor, lib
from os import path


class TestBuildMotor(unittest.TestCase):

    """Test building DMCC motors."""

    def setUp(self):
        config = path.dirname(path.realpath(__file__))+"/test_config.json"
        lib.get_config(config)

    def test_valid(self):
        """Test building a dmcc with valid param."""
        
        # Test by instanitate by id
        dmcc = DMCC(0, verify=False, bus=None)
        assert type(dmcc) is DMCC

        # Test by instanitate by address
        dmcc = DMCC(0x2d, verify=False, bus=None)
        assert type(dmcc) is DMCC

    def test_invalid_board_id(self):
        """Test proper failure for invalid motor numbers."""

        # too low an id or address
        with self.assertRaises(ValueError):
            DMCC(-1, verify=False)
       
        # to high or an id, too low for an address
        with self.assertRaises(ValueError):
            DMCC(4, verify=False)

        # to high
        with self.assertRaises(ValueError):
            DMCC(0x30, verify=False)

