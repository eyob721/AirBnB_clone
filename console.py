#!/usr/bin/python3
"""AirBnB clone - console

This is the entry point of the command interpreter

"""
import cmd

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

    def  do_show(self, args):
        """Handler for the show command"""
        
        # Check if class name is given
        if not args:
            print("** class name missing **")
            return
        
        # Check if given class name exist
        class_name = args.split(" ",1)[0]
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
        
    # HELP handlers

    def help_quit(self):
        """Help for the quit command"""
        print("Usage: quit\n" + "Quits from the console")

    def help_EOF(self):
        """Help for the EOF command"""
        print("Usage: EOF\n" + "Quits from the console")

    def help_create(self):
        """Help for the create command"""
        print(
            "Usage: create <class name>\n"
            + "Creates a new instance of the given class name, saves it to the"
            + " JSON file and prints the id"
        )


if __name__ == "__main__":
    HBNBCommand().cmdloop()
