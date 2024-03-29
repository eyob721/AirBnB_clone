#!/usr/bin/python3
"""AirBnB clone - console

This is the entry point of the command interpreter

"""
import cmd
import json
import re

from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """Class definition of the AirBnB clone - console"""

    prompt = "(hbnb) "
    __valid_classes = (
        "Amenity",
        "BaseModel",
        "City",
        "Place",
        "Review",
        "State",
        "User",
    )

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
        pattern = r"^(?P<class>\w+)?\ ?" + r"(?P<extra>.*)$"
        tokens = re.search(pattern, args).groupdict()  # type: ignore
        if not tokens["class"]:
            print("** class name missing **")
            return
        if tokens["class"] not in self.__valid_classes:
            print("** class doesn't exist **")
            return

        obj = eval("{}()".format(tokens["class"]))
        storage.save()
        print(obj.id)

    def do_show(self, args):
        """Handler for the show command"""
        pattern = (
            r"^(?P<class>\w+)?\ ?"
            + r"(?P<id>[a-zA-Z0-9\-]+)?\ ?"
            + r"(?P<extra>.*)$"
        )
        tokens = re.search(pattern, args).groupdict()  # type: ignore
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

        obj = storage.all()[key]
        print(obj)

    def do_destroy(self, args):
        """Handler for the destroy command"""
        pattern = (
            r"^(?P<class>\w+)?\ ?"
            + r"(?P<id>[a-zA-Z0-9\-]+)?\ ?"
            + r"(?P<extra>.*)$"
        )
        tokens = re.search(pattern, args).groupdict()  # type: ignore
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

        del storage.all()[key]
        storage.save()

    def do_all(self, args):
        """Handler for all command"""
        pattern = r"^(?P<class>\w+)?\ ?" + r"(?P<extra>.*)$"
        tokens = re.search(pattern, args).groupdict()  # type: ignore

        if tokens["class"] and tokens["class"] not in self.__valid_classes:
            print("** class doesn't exist **")
            return

        # build the list containig the string representation of the objects
        obj_str_list = [
            str(obj)
            for obj in storage.all().values()
            if not tokens["class"] or type(obj).__name__ == tokens["class"]
        ]

        if obj_str_list != []:
            print(obj_str_list)

    def do_update(self, args):
        """Handler for the update command"""
        pattern = (
            r"^(?P<class>\w+)?\ ?"
            + r"(?P<id>[\"\'][\w\-]*[\"\']|[\w\-]*)?\ ?"
            + r"(?P<attr>[\"\'][\w]*[\"\']|[\w]*)?\ ?"
            + r"(?P<value>[\"\'].*[\'\"]|[\w@.-]*)?\ ?"
            + r"(?P<extra>.*)$"
        )
        tokens = re.search(pattern, args).groupdict()  # pyright: ignore

        # Strip quotations
        for key in tokens:
            if type(tokens[key]) is str:
                tokens[key] = tokens[key].strip("\"'")

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

        # cast the attibute value to the attribute type
        if tokens["value"].lstrip("-").isdigit():
            tokens["value"] = int(tokens["value"])
        elif tokens["value"].lstrip("-").replace(".", "").isnumeric():
            tokens["value"] = float(tokens["value"])
        else:
            tokens["value"] = str(tokens["value"])

        obj = storage.all()[key]
        setattr(obj, tokens["attr"], tokens["value"])
        storage.save()

    def precmd(self, line):
        """Override precmd to handle commands like <class name>.cmd()"""
        line_pattern = r"^(?P<class>\w+)\.(?P<cmd>\w+)\((?P<args>.*)\)$"
        args_pattern = (
            r"^(?P<id>[\"\'][\w\-]*[\"\']|[\w\-]*)?,?\ ?"
            + r"(?P<attr>[\"\'][\w]*[\"\']|[\w]*)?,?\ ?"
            + r"(?P<value>[\"\'].*[\"\']|[\w@.-]*)?"
            + r"(?P<extra>.*)$"
        )
        line_match = re.search(line_pattern, line)
        if not line_match:
            return line

        line_tokens = line_match.groupdict()

        # <class name>.count()
        if line_tokens["cmd"] == "count":
            count = [
                type(obj).__name__ for obj in storage.all().values()
            ].count(line_tokens["class"])
            print(count)
            return ""

        args_match = re.search(args_pattern, line_tokens["args"])
        args_tokens = args_match.groupdict()  # pyright: ignore

        # <class name>.update(<id>, <dict>)
        try:
            upd_dict = json.loads(str(args_tokens["extra"]).replace("'", '"'))
        except Exception:
            upd_dict = None

        if line_tokens["cmd"] == "update" and type(upd_dict) is dict:
            for attr in upd_dict:
                self.do_update(
                    "{} {} {} '{}'".format(
                        line_tokens["class"],
                        args_tokens["id"],
                        attr,
                        str(upd_dict[attr]),
                    )
                )
            return ""

        # <class name>.cmd() -> cmds: all, show, destroy, update (without dict)
        return "{} {} {} {} {} {}".format(
            line_tokens["cmd"],
            line_tokens["class"],
            args_tokens["id"],
            args_tokens["attr"],
            args_tokens["value"],
            args_tokens["extra"],
        )

    def onecmd(self, line):
        """Override onecmd to call precmd before executing a command"""
        line = self.precmd(line)
        return super().onecmd(line)

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

    def help_update(self):
        """Help for the update command"""
        print(
            "Usage: update <class name> <id> <attribute name> <value>\n"
            + "Updates an instance based on the class name and id by "
            + "adding or updating an attribute.\n"
            + "The change is saved to the JSON file."
            + "The value is type casted when it is assigned and "
            + "all extra arguments are ignored."
        )


if __name__ == "__main__":
    HBNBCommand().cmdloop()
