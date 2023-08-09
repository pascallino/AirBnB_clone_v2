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
        quit = r"Quit command to exit the program."
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help quit'))
            self.assertEqual(quit, out.getvalue().strip())

    def test_help_EOF(self):
        eof = "End of File"
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help EOF'))
            self.assertEqual(eof, out.getvalue().strip())

    def test_help_destroy(self):
        des = "Deletes an object from file.json"
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help destroy'))
            self.assertEqual(des, out.getvalue().strip())

    def test_help_show(self):
        sh = """Prints the string representation of an \
                instance based on the class name and id"""
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help show'))
            self.assertEqual(sh, out.getvalue().strip())

    def test_help_all(self):
        all = """<class name>.all(), all, all <class name>"""
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help all'))
            self.assertEqual(all, out.getvalue().strip())

    def test_help_update(self):
        upt = """Usage: update <class name> <id>
        <attribute name> "<attribute value>"""
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help update'))
            self.assertEqual(upt, out.getvalue().strip())

    def test_help_create(self):
        ct = """Ex: $ create User/State create an object class with an id""" 
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help create'))
            self.assertEqual(ct, out.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
