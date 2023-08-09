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
            bmkey = f"BaseModel.{output.getvalue().strip()}"
            self.assertIn(bmkey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(output.getvalue().strip()))
            userkey = f"User.{output.getvalue().strip()}"
            self.assertIn(userkey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(output.getvalue().strip()))
            statekey = f"State.{output.getvalue().strip()}"
            self.assertIn(statekey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(output.getvalue().strip()))
            cityKey = f"City.{output.getvalue().strip()}"
            self.assertIn(cityKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(output.getvalue().strip()))
            amdKey = f"Amenity.{output.getvalue().strip()}"
            self.assertIn(amdKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(output.getvalue().strip()))
            placeKey = f"Place.{output.getvalue().strip()}"
            self.assertIn(placeKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(output.getvalue().strip()))
            RvKey = f"Review.{output.getvalue().strip()}"
            self.assertIn(RvKey, storage.all().keys())


class TestHBNBCommand_show(unittest.TestCase):
    """ test for show command and output """

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

    def test_show_missing_class_name_error(self):
        """ test for missing class name """
        errormsg = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_show_wrong_class(self):
        """ test for class existence """
        errormsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show basemodel"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("basemodel.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_show_missing_id(self):
        """ test for no instance id"""
        errormsg = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_show_missing_id_within_brackets(self):
        """ test <class name>.show(id) if id is missing """
        errormsg = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_show_output_for_objects_dict(self):
        """ test show for new objects created """
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            bmID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(bmID)]
            command = "show BaseModel {}".format(bmID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            RvID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(RvID)]
            command = "show Review {}".format(RvID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            stateID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(stateID)]
            command = "show State {}".format(stateID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            UID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(UID)]
            command = "show User {}".format(UID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            AmdID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(AmdID)]
            command = "show Amenity {}".format(AmdID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            PlaceID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(PlaceID)]
            command = "show Place {}".format(PlaceID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            CityID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(CityID)]
            command = "show City {}".format(CityID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())

    def test_show_no_instance_found_in_parenthesis(self):
        """ test for instance found in show parenthesis """
        errormsg = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show(7979)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show(6864)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show(9089)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show(1467)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show(3421)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show(9453)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show(23129)"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_show_no_instance_found(self):
        """ test no instance found for show method """
        errormsg = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 1876867567"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User 908787"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State 5755453"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City 0997656"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 357668"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place 796564"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review 966567"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_show_output_for_objects_keys_InParenthesis(self):
        """ test show.(id) output """
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            bmID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(bmID)]
            command = "BaseModel.show({})".format(bmID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            UID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(UID)]
            command = "User.show({})".format(UID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            stateID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(stateID)]
            command = "State.show({})".format(stateID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            RvID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(RvID)]
            command = "Review.show({})".format(RvID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            CityID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(CityID)]
            command = "City.show({})".format(CityID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            PID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(PID)]
            command = "Place.show({})".format(PID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            AmdID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(AmdID)]
            command = "Amenity.show({})".format(AmdID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())


class TestHBNBCommand_all(unittest.TestCase):
    """ all command test cases """
    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_all_class_doesnt_exit(self):
        """ test class doent exist for all <class name> """
        errormsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Pascal"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Pascal.all()"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_all_objects_withoutclass_withparenthesis(self):
        """ test display of all objet Usage .all()"""
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".all()"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertIn("User", output.getvalue().strip())
            self.assertIn("State", output.getvalue().strip())
            self.assertIn("Place", output.getvalue().strip())
            self.assertIn("City", output.getvalue().strip())
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertIn("Review", output.getvalue().strip())

    def test_all_objects_display(self):
        """ test for all objects display """
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertIn("User", output.getvalue().strip())
            self.assertIn("State", output.getvalue().strip())
            self.assertIn("Place", output.getvalue().strip())
            self.assertIn("City", output.getvalue().strip())
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertIn("Review", output.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
