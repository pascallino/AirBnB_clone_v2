#!/usr/bin/python3
""" unit test for the HBNB Console

unittest class:
    TestHBNBCommand_prompting
    """
import sys
import os
import unittest
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestHBNBCommand_prompt(unittest.TestCase):
    """ testing the prompt for the interpreter """

    def test_prompt_string(self):
        """ test prompt string """
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_emptyline(self):
        """ test empty line """
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd(''))
            self.assertEqual("", out.getvalue().strip())


class TestHBNBCommand_help(unittest.TestCase):
    """ testing quit for the interpreter """

    def test_help_quit(self):
        tq = r"Quit command to exit the program."
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help quit'))
            self.assertEqual(tq, out.getvalue().strip())

    def test_help_EOF(self):
        eof = "End of File"
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help EOF'))
            self.assertEqual(eof, out.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
