#!/usr/bin/python3
"""Tests for the AirBnB clone - console"""
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from console import HBNBCommand


def get_cmd_output(command: str):
    """Returns the output string from stdout of a console command"""
    with patch("sys.stdout", new=StringIO()) as output:
        HBNBCommand().onecmd(command)
        return output.getvalue()


class TestHBNBCommandHandlers(TestCase):
    """Tests for command handlers of the console"""

    def test_prompt(self):
        self.assertEqual(HBNBCommand.prompt, "(hbnb) ")

    def test_emptyline(self):
        output_exp = ""

        output_got = get_cmd_output("")
        self.assertEqual(
            output_exp, output_got, msg="emptyline output is not correct"
        )

        output_got = get_cmd_output("   \n\n\n")
        self.assertEqual(
            output_exp, output_got, msg="emptyline output is not correct"
        )

    def test_quit(self):
        self.assertEqual(
            HBNBCommand().onecmd("quit"),
            True,
            msg="quit command must return True",
        )

        output_exp = ""
        output_got = get_cmd_output("quit")
        self.assertEqual(
            output_got, output_exp, msg="quit output is not correct"
        )

    def test_EOF(self):
        self.assertEqual(
            HBNBCommand().onecmd("EOF"),
            True,
            msg="EOF command must return True",
        )

        output_exp = "\n"
        output_got = get_cmd_output("EOF")
        self.assertEqual(
            output_got, output_exp, msg="EOF output is not correct"
        )


class TestHBNBCommandHelps(TestCase):
    """Tests for the helps sections of the console"""

    def test_help(self):
        output_exp = """
Documented commands (type help <topic>):
========================================
EOF  help  quit

"""
        output_got = get_cmd_output("help")
        self.assertEqual(
            output_got, output_exp, msg="help output is not correct"
        )
