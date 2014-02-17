"""Test cases for lib module."""

from unittest import TestCase

from os import path
import logging
import pyDMCC.lib as lib

DIR_NAME = path.dirname(path.realpath(__file__))

class TestGetConfig(TestCase):

    """Test loading configuration."""

    def test_config_type(self):
        """Confirm that type of config is a dict."""
        config = lib.get_config(DIR_NAME + "/test_config.json")
        assert type(config) is dict

    def test_invalid_filename(self):
        """Test proper failure for fake config file."""
        with self.assertRaises(IOError):
            config = lib.get_config("does_not_exist.json")

    def test_config_contents(self):
        """Confirm that config dict has the right keys"""
        config = lib.get_config(DIR_NAME + "/test_config.json")
        self.assertNotIn('foo', config)
        self.assertEqual(config['test'], 1234)

        config = lib.get_config(DIR_NAME + "/test_config_alt.json")
        self.assertNotIn('test', config)
        self.assertEqual(config['test2'], 5678)


class TestGetLogger(TestCase):

    """Test getting a logger object."""

    def setUp(self):
        config = lib.get_config(DIR_NAME + "/test_config.json")

    def test_type(self):
        """Test that object returned is of proper type."""
        assert type(lib.get_logger()) is logging.Logger
