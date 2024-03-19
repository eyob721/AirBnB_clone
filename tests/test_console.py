#!/usr/bin/python3
"""Tests for the AirBnB clone - console"""
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from console import HBNBCommand
from models import storage
from models.base_model import BaseModel


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

    def test_create(self):
        # check for missing class name
        output_exp = "** class name missing **\n"
        output_got = get_cmd_output("create")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when class name is missing",
        )

        # check for invalid class name
        output_exp = "** class doesn't exist **\n"
        output_got = get_cmd_output("create MyModel")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when class doesn't exist",
        )

        # check for a valid classes
        output_exp = r"^\w+-\w+-\w+-\w+-\w+$\n"
        # TODO: add more classes later on
        valid_classes = ("BaseModel",)
        for _class in valid_classes:
            output_got = get_cmd_output(f"create {_class}")
            self.assertRegex(
                output_got,
                output_exp,
                msg=f"incorrect output when valid class ({_class}) is given",
            )
            key = "{}.{}".format(_class, output_got.rstrip("\n"))
            self.assertIn(key, storage.all())

    def test_show(self):
        # check for missing class name
        output_exp = "** class name missing **\n"
        output_got = get_cmd_output("show")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when class name is missing",
        )

        # check for invalid class name
        output_exp = "** class doesn't exist **\n"
        output_got = get_cmd_output("show MyModel")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when class doesn't exist",
        )

        # check for missing id
        output_exp = "** instance id missing **\n"
        output_got = get_cmd_output("show BaseModel")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when id is missing",
        )

        # check for missing instance (invalid id)
        output_exp = "** no instance found **\n"
        output_got = get_cmd_output("show BaseModel 123")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when instance is not found (invalid id)",
        )

        # check for a correct usage
        b = BaseModel()
        output_exp = str(b) + "\n"
        output_got = get_cmd_output(f"show BaseModel {b.id}")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output for correct usage",
        )

        # check for a extra arguments
        b = BaseModel()
        output_exp = str(b) + "\n"
        output_got = get_cmd_output(f"show BaseModel {b.id}")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output for correct usage",
        )

    def test_delete(self):
        # check for missing class name
        output_exp = "** class name missing **\n"
        output_got = get_cmd_output("delete")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when class name is missing",
        )

        # check for invalid class name
        output_exp = "** class doesn't exist **\n"
        output_got = get_cmd_output("delete MyModel")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when class doesn't exist",
        )

        # check for missing id
        output_exp = "** instance id missing **\n"
        output_got = get_cmd_output("delete BaseModel")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when id is missing",
        )

        # check for missing instance (invalid id)
        output_exp = "** no instance found **\n"
        output_got = get_cmd_output("delete BaseModel 123")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when instance is not found (invalid id)",
        )

        # check for a correct usage
        b = BaseModel()
        key = f"BaseModel.{b.id}"
        HBNBCommand().onecmd(f"delete BaseModel {b.id}")
        self.assertNotIn(
            key,
            storage.all().keys(),
            msg="instance not deleted",
        )

        # check with extra arguments
        b = BaseModel()
        key = f"BaseModel.{b.id}"
        HBNBCommand().onecmd(f"delete BaseModel {b.id} hello from Alx")
        self.assertNotIn(
            key,
            storage.all().keys(),
            msg="instance not deleted",
        )


class TestHBNBCommandHelps(TestCase):
    """Tests for the helps sections of the console"""

    def test_help(self):
        output_exp = """
Documented commands (type help <topic>):
========================================
EOF  create  delete  help  quit  show

"""
        output_got = get_cmd_output("help")
        self.assertEqual(
            output_got, output_exp, msg="<help> output is not correct"
        )

    def test_help_quit(self):
        output_exp = "Usage: quit\n" + "Quits from the console\n"
        output_got = get_cmd_output("help quit")
        self.assertEqual(
            output_got, output_exp, msg="<help quit> output is not correct"
        )

    def test_help_EOF(self):
        output_exp = "Usage: EOF\n" + "Quits from the console\n"
        output_got = get_cmd_output("help EOF")
        self.assertEqual(
            output_got, output_exp, msg="<help EOF> output is not correct"
        )

    def test_help_create(self):
        output_exp = (
            "Usage: create <class name>\n"
            + "Creates a new instance of the given class name, saves it to the"
            + " JSON file and prints the id\n"
        )
        output_got = get_cmd_output("help create")
        self.assertEqual(
            output_got, output_exp, msg="<help create> output is not correct"
        )

    def test_help_show(self):
        output_exp = (
            "Usage: show <class name> <id>\n"
            + "Prints the string representation of an instance, based on the "
            + "class name and id\n"
        )
        output_got = get_cmd_output("help show")
        self.assertEqual(
            output_got, output_exp, msg="<help show> output is not correct"
        )

    def test_help_delete(self):
        output_exp = (
            "Usage: delete <class name> <id>\n"
            + "Deletes an instance based on the class name and id, and saves "
            + "the change into the JSON file\n"
        )
        output_got = get_cmd_output("help delete")
        self.assertEqual(
            output_got, output_exp, msg="<help delete> output is not correct"
        )
