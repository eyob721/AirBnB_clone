#!/usr/bin/python3
"""AirBnB clone - console

This is the entry point of the command interpreter

"""
import cmd


class HBNBCommand(cmd.Cmd):
    """Class definition of the AirBnB clone - console"""

    prompt = "(hbnb) "

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

    # HELP handlers

    def help_quit(self):
        """Help for the quit command"""
        print("Usage: quit\n" + "Quits from the console")

    def help_EOF(self):
        """Help for the EOF command"""
        print("Usage: EOF\n" + "Quits from the console")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
