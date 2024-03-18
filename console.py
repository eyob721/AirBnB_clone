#!/usr/bin/python3
"""AirBnB clone - console"""
import cmd

class HBNBCommand(cmd.Cmd):
    
    prompt = "(hbnb) "
    
    def do_quit(self, args):
        return True

    def do_EOF(self, args):
        return True

    def emptyline(self):
        pass

    def help_quit(self, args):
        print("Quit the console")

    def help_EOF(self, args):
        print("Handles EOF")    
    
if __name__ == '__main__':
    HBNBCommand().cmdloop()