"""Test cases for lib module."""

import logging
import unittest

import lib.lib as lib


class TestGetConfig(unittest.TestCase):

    """Test loading configuration."""

    def test_type(self):
        """Confirm that type of config is a dict."""
        config = lib.get_config()
        assert type(config) is dict

    def test_invalid(self):
        """Test proper failure for fake config file."""
        with self.assertRaises(IOError):
            config = lib.get_config("fake.yaml")


class TestGetLogger(unittest.TestCase):

    """Test getting a logger object."""

    def test_type(self):
        """Test that object returned is of proper type."""
        assert type(lib.get_logger()) is logging.Logger
