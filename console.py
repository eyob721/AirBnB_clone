#!/usr/bin/python3
"""AirBnB clone - console

This is the entry point of the command interpreter

"""
import cmd
import re

from models import storage
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """Class definition of the AirBnB clone - console"""

    prompt = "(hbnb) "
    __valid_classes = ("BaseModel",)

    # COMMAND handlers

    def do_quit(self, args):
        """Handler for the quit command"""
        return True

    def do_EOF(self, args):
        """Handler for end-of-file signal"""
        print()
        return True

    def emptyline(self):
        """Handler for empty line + ENTER"""
        pass

    def do_create(self, args):
        """Handler for the create command"""

        # Check if class name is given
        if not args:
            print("** class name missing **")
            return

        # Check if given class name exists
        class_name = args.split(" ", 1)[0]
        if class_name not in self.__valid_classes:
            print("** class doesn't exist **")
            return

        # Class exists, create an instance
        obj = eval(f"{class_name}()")
        storage.save()
        print(obj.id)

    def do_show(self, args):
        """Handler for the show command"""

        # Check if class name is given
        if not args:
            print("** class name missing **")
            return

        # Check if given class name exist
        class_name = args.split(" ", 1)[0]
        if class_name not in self.__valid_classes:
            print("** class doesn't exist **")
            return

        # Check if id is given
        if len(args.split(" ")) == 1:
            print("** instance id missing **")
            return

        # If id is given, check instance exists
        id = args.split(" ", 2)[1]
        key = f"{class_name}.{id}"
        if key not in storage.all():
            print("** no instance found **")
            return

        # If instance exists, print it's string representation
        obj = storage.all()[key]
        print(obj)

    def do_destroy(self, args):
        """Handler for the destroy command"""

        # Check if class name is given
        if not args:
            print("** class name missing **")
            return

        # Check if given class name exist
        class_name = args.split(" ", 1)[0]
        if class_name not in self.__valid_classes:
            print("** class doesn't exist **")
            return

        # Check if id is given
        if len(args.split(" ")) == 1:
            print("** instance id missing **")
            return

        # If id is given, check instance exists
        id = args.split(" ", 2)[1]
        key = f"{class_name}.{id}"
        if key not in storage.all():
            print("** no instance found **")
            return

        # If instance exists, destroy it
        del storage.all()[key]
        storage.save()

    def do_update(self, args):
        """Handler for the update command"""
        parser = re.compile(
            r"^(?P<class>\w+)?\ ?"
            + r"(?P<id>[a-zA-Z0-9\-]+)?\ ?"
            + r"(?P<attr>[a-zA-Z0-9_]+)?\ ?"
            + r"(?P<value>[\"\']?[a-zA-Z0-9\.@\- ]+[\"\']?)?"
            + r"(?P<extra>.*)$"
        )
        tokens = parser.search(args).groupdict()  # type: ignore

        if not tokens["class"]:
            print("** class name missing **")
            return

        if tokens["class"] not in self.__valid_classes:
            print("** class doesn't exist **")
            return

        if not tokens["id"]:
            print("** instance id missing **")
            return

        key = "{}.{}".format(tokens["class"], tokens["id"])
        if key not in storage.all():
            print("** no instance found **")
            return

        if not tokens["attr"]:
            print("** attribute name missing **")
            return

        if not tokens["value"]:
            print("** value missing **")
            return

        # Cast the attibute value to the attribute type
        if tokens["value"].lstrip("-").isdigit():
            tokens["value"] = int(tokens["value"])
        elif tokens["value"].lstrip("-").replace(".", "").isnumeric():
            tokens["value"] = float(tokens["value"])
        else:
            tokens["value"] = tokens["value"].strip("\"'")

        obj = storage.all()[key]
        setattr(obj, tokens["attr"], tokens["value"])
        storage.save()

    def do_all(self, args):
        """Handler for all command"""

        # When no argument is given, print all objects of all classes
        if not args:
            obj_list = [str(obj) for obj in storage.all().values()]
            print(obj_list)
            return

        # Check if the given class name exists
        class_name = args.split(" ", 1)[0]
        if class_name not in self.__valid_classes:
            print("** class doesn't exist **")
            return

        # If class exists, print all object with that class
        obj_list = [
            str(obj)
            for obj in storage.all().values()
            if type(obj).__name__ == class_name
        ]
        print(obj_list)

    # HELP handlers

    def help_quit(self):
        """Help for the quit command"""
        print("Usage: quit\n" + "Quits from the console.")

    def help_EOF(self):
        """Help for the EOF command"""
        print(
            "Usage: EOF\n" + "Handles end-of-file signal. Exits the program."
        )

    def help_create(self):
        """Help for the create command"""
        print(
            "Usage: create <class name>\n"
            + "Creates a new instance of the given class name, saves it to the"
            + " JSON file and prints the id."
        )

    def help_show(self):
        """Help for the show command"""
        print(
            "Usage: show <class name> <id>\n"
            + "Prints the string representation of an instance, based on the "
            + "class name and id."
        )

    def help_destroy(self):
        """Help for the destroy command"""
        print(
            "Usage: destroy <class name> <id>\n"
            + "Destroys an instance based on the class name and id, and saves "
            + "the change into the JSON file."
        )

    def help_all(self):
        """Help for the all command"""
        print(
            "Usage: all [class name]\n"
            + "Prints the string representation of all instances.\n"
            + "With class name, then only string representation of instances "
            + "with that class will be printed."
        )


if __name__ == "__main__":
    HBNBCommand().cmdloop()
