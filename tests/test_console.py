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
from models import storage
from models.engine.file_storage import FileStorage


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


class TestHBNBCommand_create(unittest.TestCase):
    """ test for create command and output """

    @classmethod
    def setUp(self):
        """ before the test begin call the setUp method"""
        try:
            os.rename("file.json", "pascal")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        """ After test complet call the tearDown method """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    def test_create_missing_class_name_error(self):
        """ test for missing class name"""
        errormsg = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_create_wrong_class(self):
        """ test for invalid class """
        errormsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Pascal"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_create_wrong_command(self):
        """ test for wrong command"""
        errormsg = "*** Unknown syntax: classes"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("classes"))
            self.assertEqual(errormsg, output.getvalue().strip())
        errormsg = "*** Unknown syntax: BaseModel2"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel2"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_create_different_objects(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(output.getvalue().strip()))
            bmid = f"BaseModel.{output.getvalue().strip()}"
            self.assertIn(bmid, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(output.getvalue().strip()))
            uid = f"User.{output.getvalue().strip()}"
            self.assertIn(uid, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(output.getvalue().strip()))
            stateid = f"State.{output.getvalue().strip()}"
            self.assertIn(stateid, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "City.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "Amenity.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "Place.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "Review.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())


if __name__ == '__main__':
    unittest.main()
