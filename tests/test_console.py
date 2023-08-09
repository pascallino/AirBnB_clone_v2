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

    def test_help_count(self):
        cnt = """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help count'))
            self.assertEqual(cnt, out.getvalue().strip())

    def test_help_help(self):
        help = "List available commands with \"help\" "\
                "or detailed help with \"help cmd\"."
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help help'))
            self.assertEqual(help, out.getvalue().strip())

    def test_help(self):
        help = ("Documented commands (type help <topic>):\n"
                "========================================\n"
                "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(help, output.getvalue().strip())


class TestHBNBCommand_quit(unittest.TestCase):
    """ Test EOF and quit for the cmd interpreter """

    def test_EOF(self):
        """ End of file test """
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))

    def test_quit(self):
        """ quit the program """
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))


if __name__ == '__main__':
    unittest.main()
