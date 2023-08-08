#!/usr/bin/python3
""" BackEnd Interpreter for HBnB console. """
import re
import cmd
import sys
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


def tokenize(line):
    """ tokenize : converts the line into tuples and last
    element is always the full line"""
    return [i.strip(",") for i in split(line)]


class HBNBCommand(cmd.Cmd):
    """ Configures the command Interpreter for Holberton app """
    prompt = "(hbnb) "
    __classes = [
            "BaseModel",
            "User",
            "State",
            "City",
            "Place",
            "Amenity",
            "Review"]
    # intro = 'Simple Command Interpreter for the holberton Web app'

    def do_EOF(self, arg):
        """ End of File """
        print("")
        return True

    def do_quit(self, arg):
        """Quit command to exit the program.\n"""
        return True

    def emptyline(self):
        """ Empty line triggered """
        pass

    def do_create(self, arg):
        """Ex: $ create BaseModel
        create an object class with an id """
        args = tokenize(arg)
        if len(args) == 0:
            print("** class name missing **")
        else:
            if not args[0] in self.__classes:
                print("** class doesn't exist **")
            else:
                print(eval(args[0])().id)
                storage.save()

    def do_show(self, arg):
        """ Prints the string representation of an
        instance based on the class name and id
        """
        args = tokenize(arg)
        loadallobj = storage.all()
        if len(args) > 1:
            clName_id = f"{args[0]}.{args[1]}"
        if len(args) == 0:
            print("** class name missing **")
        else:
            if not args[0] in self.__classes:
                print("** class doesn't exist **")
            elif len(args) == 1:
                print("** instance id missing **")
            elif clName_id not in loadallobj:
                print("** no instance found **")
            else:
                print(loadallobj[clName_id])

    def do_destroy(self, arg):
        """ Prints the string representation of an
        instance based on the class name and id
        """
        args = tokenize(arg)
        loadallobj = storage.all()
        if len(args) > 1:
            clName_id = f"{args[0]}.{args[1]}"
        if len(args) == 0:
            print("** class name missing **")
        else:
            if not args[0] in self.__classes:
                print("** class doesn't exist **")
            elif len(args) == 1:
                print("** instance id missing **")
            elif clName_id not in loadallobj:
                print("** no instance found **")
            else:
                del loadallobj[clName_id]
                storage.save()

    def do_all(self, arg):
        """Prints all string representation of all
        instances based or not on the class name.
        <class name>.all(), all, all <class name>
        """
        objlist = []
        args = tokenize(arg)
        loadallobj = storage.all()
        if len(args) >= 1:
            if not args[0] in self.__classes:
                print("** class doesn't exist **")
            else:
                for obj in loadallobj.values():
                    if obj.__class__.__name__ == args[0]:
                        objlist.append(obj.__str__())
                print(objlist)
        else:
            for obj in loadallobj.values():
                objlist.append(obj.__str__())
            print(objlist)

    def do_update(self, arg):
        """Usage: update <class name> <id>
        <attribute name> "<attribute value>"""
        args = tokenize(arg)
        loadallobj = storage.all()
        print(len(args))
        if len(args) > 1:
            clName_id = f"{args[0]}.{args[1]}"
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(args) == 1:
            print("** instance id missing **")
            return False
        if clName_id not in loadallobj:
            print("** no instance found **")
            return False
        if len(args) == 2:
            print("** attribute name missing **")
            return False
        if len(args) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(args) == 4:
            upt = loadallobj[clName_id]
            if args[2] in upt.__class__.__dict__.keys():
                valdatatype = type(upt.__class__.__dict__[args[2]])
                upt.__dict__[args[2]] = valdatatype(args[3])
            else:
                upt.__dict__[args[2]] = args[3]
        elif len(args) == 3 and type(eval(argl[2])) == dict:
            upt = loadallobj[clName_id]
            keylist = upt.__class__.__dict__
            for key, value in eval(argl[2]).items():
                if (key in keylist.keys() and
                        type(keylist[key]) in [str, int, float]):
                    valdatatype = type(upt.__class__.__dict__[key])
                    upt.__dict__[key] = valdatatype(value)
                else:
                    upt.__dict__[key] = value
        storage.save()

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        args = tokenize(arg)
        count = 0
        for Allobj in storage.all().values():
            if args[0] == Allobj.__class__.__name__:
                count += 1
        print(count)

    def default(self, arg):
        """cmd default behavior for cmd module when input is invalid"""
        func = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update,
            "count": self.do_count
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                cmd = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if cmd[0] != "update":
                    match = re.search(r"\((.*?)\)", argl[1])
                    argl[1] = match.group()[2:-2]
                elif cmd[0] == "update":
                    au = [i.strip(",") for i in split(match.group()[1:-1])]
                if cmd[0] in func.keys():
                    if len(argl[1]) > 20 and not cmd[0] == "update":
                        call = f"{argl[0]} {argl[1]} {cmd[0]}"
                    elif cmd[0] == "update":
                        call = f"{argl[0]} {au[0]} {au[1]} {au[2]}"
                    else:
                        call = f"{argl[0]} {cmd[0]}"
                    return func[cmd[0]](call)
        print("*** Unknown syntax: {}".format(arg))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
