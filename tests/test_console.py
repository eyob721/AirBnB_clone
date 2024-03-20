#!/usr/bin/python3
"""Tests for the AirBnB clone - console"""
import os
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


class TestHBNBCommand(TestCase):
    """Tests for the console"""

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


class TestHBNBCommandCreate(TestCase):
    """Tests for the create command"""

    def test_create_missing_class_name(self):
        output_exp = "** class name missing **\n"
        output_got = get_cmd_output("create")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when class name is missing",
        )

    def test_create_invalid_class_name(self):
        # check for invalid class name
        output_exp = "** class doesn't exist **\n"
        output_got = get_cmd_output("create MyModel")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when class doesn't exist",
        )

    def test_create_correct_usage(self):
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


class TestHBNBCommandShow(TestCase):
    """Tests for the show command"""

    def test_show_missing_class_name(self):
        output_exp = "** class name missing **\n"
        output_got = get_cmd_output("show")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when class name is missing",
        )

    def test_show_invalid_class_name(self):
        output_exp = "** class doesn't exist **\n"
        output_got = get_cmd_output("show MyModel")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when class doesn't exist",
        )

    def test_show_missing_id(self):
        output_exp = "** instance id missing **\n"
        output_got = get_cmd_output("show BaseModel")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when id is missing",
        )

    def test_show_missing_instance(self):
        output_exp = "** no instance found **\n"
        output_got = get_cmd_output("show BaseModel 123")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when instance is not found (invalid id)",
        )

    def test_show_correct_usage(self):
        b = BaseModel()
        output_exp = str(b) + "\n"
        output_got = get_cmd_output(f"show BaseModel {b.id}")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output for correct usage",
        )

    def test_show_correct_usage_with_extra_arguments(self):
        # extra arguments should be ignored
        b = BaseModel()
        output_exp = str(b) + "\n"
        output_got = get_cmd_output(f"show BaseModel {b.id}")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output for correct usage",
        )


class HBNBCommandDestroy(TestCase):
    """Tests for the destroy command"""

    def test_destroy_missing_class_name(self):
        output_exp = "** class name missing **\n"
        output_got = get_cmd_output("destroy")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when class name is missing",
        )

    def test_destroy_invalid_class_name(self):
        output_exp = "** class doesn't exist **\n"
        output_got = get_cmd_output("destroy MyModel")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when class doesn't exist",
        )

    def test_destroy_missing_id(self):
        output_exp = "** instance id missing **\n"
        output_got = get_cmd_output("destroy BaseModel")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when id is missing",
        )

    def test_destroy_missing_instance(self):
        output_exp = "** no instance found **\n"
        output_got = get_cmd_output("destroy BaseModel 123")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when instance is not found (invalid id)",
        )

    def test_destroy_correct_usage(self):
        b = BaseModel()
        key = f"BaseModel.{b.id}"
        HBNBCommand().onecmd(f"destroy BaseModel {b.id}")
        self.assertNotIn(
            key,
            storage.all().keys(),
            msg="instance not destroyd",
        )

    def test_destroy_correct_usage_with_extra_arguments(self):
        # extra arguments should be ignored
        b = BaseModel()
        key = f"BaseModel.{b.id}"
        HBNBCommand().onecmd(f"destroy BaseModel {b.id} hello from Alx")
        self.assertNotIn(
            key,
            storage.all().keys(),
            msg="instance not destroyd",
        )


class HBNBCommandAll(TestCase):
    """Tests for the all command"""

    def test_all_invalid_class_name(self):
        output_exp = "** class doesn't exist **\n"
        output_got = get_cmd_output("all MyModel")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when class doesn't exist",
        )

    def test_all_without_class_name(self):
        obj_list = [str(obj) for obj in storage.all().values()]
        output_exp = str(obj_list) + "\n"
        output_got = get_cmd_output("all")
        self.assertEqual(
            output_got, output_exp, msg="incorrect output for `$ all`"
        )

    def test_all_with_class_name(self):
        valid_classes = ("BaseModel",)
        for _class in valid_classes:
            obj_list = [
                str(obj)
                for obj in storage.all().values()
                if type(obj).__name__ == _class
            ]
            output_exp = str(obj_list) + "\n"
            output_got = get_cmd_output(f"all {_class}")
            self.assertEqual(
                output_got,
                output_exp,
                msg=f"incorrect output for `$ all {_class}`",
            )


class TestHBNBCommandUpdate(TestCase):
    """Tests for the update command"""

    def test_update_missing_class_name(self):
        output_exp = "** class name missing **\n"
        output_got = get_cmd_output("update")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when class name is missing",
        )

    def test_update_invalid_class_name(self):
        output_exp = "** class doesn't exist **\n"
        output_got = get_cmd_output("update MyModel")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when class doesn't exist",
        )

    def test_update_missing_id(self):
        output_exp = "** instance id missing **\n"
        output_got = get_cmd_output("update BaseModel")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when id is missing",
        )

    def test_update_missing_instance(self):
        output_exp = "** no instance found **\n"
        output_got = get_cmd_output("update BaseModel 123")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when instance is not found (invalid id)",
        )

    def test_update_missing_attribute(self):
        b = BaseModel()
        output_exp = "** attribute name missing **\n"
        output_got = get_cmd_output(f"update BaseModel {b.id}")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when attribute name is missing",
        )

    def test_update_missing_value(self):
        b = BaseModel()
        output_exp = "** value missing **\n"
        output_got = get_cmd_output(f"update BaseModel {b.id} eg")
        self.assertEqual(
            output_got,
            output_exp,
            msg="incorrect output when value is missing",
        )

    def test_update_correct_usages(self):
        b = BaseModel()

        cases = {
            "name": '"John Doe"',
            "gender": "M",
            "age": 47,
            "height": 1.82,
            "email": '"john@gmail.com"',
        }

        for attr in cases.keys():
            HBNBCommand().onecmd(
                "update BaseModel {} {} {}".format(b.id, attr, cases[attr])
            )
            # Check that attribute is set
            self.assertIn(attr, b.to_dict(), msg="attribute not found")
            if type(cases[attr]) is str:
                self.assertEqual(
                    getattr(b, attr),
                    cases[attr].strip("\"'"),
                    msg="correct value not set",
                )
            else:
                self.assertEqual(
                    getattr(b, attr), cases[attr], msg="correct value not set"
                )

            # Check that attribute value is properly casted
            self.assertIs(
                type(getattr(b, attr)),
                type(cases[attr]),
                msg="attribute value not properly casted",
            )

        # Check that it is saved
        storage.reload()
        key = f"BaseModel.{b.id}"
        obj = storage.all()[key]
        obj_dict = obj.to_dict()

        for attr in cases:
            self.assertIn(
                attr, obj_dict, msg="attribute not found in saved object"
            )
            if type(cases[attr]) is str:
                self.assertEqual(
                    getattr(obj, attr),
                    cases[attr].strip("\"'"),
                    msg="correct value not set",
                )
            else:
                self.assertEqual(
                    getattr(obj, attr),
                    cases[attr],
                    msg="correct value not set",
                )

            # Check that attribute value is properly casted
            self.assertIs(
                type(getattr(obj, attr)),
                type(cases[attr]),
                msg="attribute value not properly casted in saved object",
            )

    def test_update_correct_usage_with_extra_args(self):
        b = BaseModel()

        HBNBCommand().onecmd(
            f"update BaseModel {b.id} name 'John Doe' this is extra"
        )
        self.assertIn("name", b.to_dict(), msg="attribute not found")
        self.assertEqual(
            getattr(b, "name"), "John Doe", msg="correct value not set"
        )
        self.assertIs(
            type(getattr(b, "name")),
            str,
            msg="attribute value not properly casted",
        )

        HBNBCommand().onecmd(f"update BaseModel {b.id} age 47 this is extra")
        self.assertIn("age", b.to_dict(), msg="attribute not found")
        self.assertEqual(getattr(b, "age"), 47, msg="correct value not set")
        self.assertIs(
            type(getattr(b, "age")),
            int,
            msg="attribute value not properly casted",
        )

        HBNBCommand().onecmd(
            f"update BaseModel {b.id} height 3.14 this is extra"
        )
        self.assertIn("height", b.to_dict(), msg="attribute not found")
        self.assertEqual(
            getattr(b, "height"), 3.14, msg="correct value not set"
        )
        self.assertIs(
            type(getattr(b, "height")),
            float,
            msg="attribute value not properly casted",
        )


class TestHBNBCommandHelps(TestCase):
    """Tests for the helps sections of the console"""

    def test_help(self):
        output_exp = """
Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

"""
        output_got = get_cmd_output("help")
        self.assertEqual(
            output_got, output_exp, msg="<help> output is not correct"
        )

    def test_help_quit(self):
        output_exp = "Usage: quit\n" + "Quits from the console.\n"
        output_got = get_cmd_output("help quit")
        self.assertEqual(
            output_got, output_exp, msg="<help quit> output is not correct"
        )

    def test_help_EOF(self):
        output_exp = (
            "Usage: EOF\n" + "Handles end-of-file signal. Exits the program.\n"
        )
        output_got = get_cmd_output("help EOF")
        self.assertEqual(
            output_got, output_exp, msg="<help EOF> output is not correct"
        )

    def test_help_create(self):
        output_exp = (
            "Usage: create <class name>\n"
            + "Creates a new instance of the given class name, saves it to the"
            + " JSON file and prints the id.\n"
        )
        output_got = get_cmd_output("help create")
        self.assertEqual(
            output_got, output_exp, msg="<help create> output is not correct"
        )

    def test_help_show(self):
        output_exp = (
            "Usage: show <class name> <id>\n"
            + "Prints the string representation of an instance, based on the "
            + "class name and id.\n"
        )
        output_got = get_cmd_output("help show")
        self.assertEqual(
            output_got, output_exp, msg="<help show> output is not correct"
        )

    def test_help_destroy(self):
        output_exp = (
            "Usage: destroy <class name> <id>\n"
            + "Destroys an instance based on the class name and id, and saves "
            + "the change into the JSON file.\n"
        )
        output_got = get_cmd_output("help destroy")
        self.assertEqual(
            output_got, output_exp, msg="<help destroy> output is not correct"
        )

    def test_help_all(self):
        output_exp = (
            "Usage: all [class name]\n"
            + "Prints the string representation of all instances.\n"
            + "With class name, then only string representation of instances "
            + "with that class will be printed.\n"
        )
        output_got = get_cmd_output("help all")
        self.assertEqual(
            output_got, output_exp, msg="<help all> output is not correct"
        )

    def test_help_update(self):
        output_exp = (
            "Usage: update <class name> <id> <attribute name> <value>\n"
            + "Updates an instance based on the class name and id by "
            + "adding or updating an attribute.\n"
            + "The change is saved to the JSON file."
            + "The value is type casted when it is assigned and "
            + "all extra arguments are ignored.\n"
        )
        output_got = get_cmd_output("help update")
        self.assertEqual(
            output_got, output_exp, msg="<help update> output is not correct"
        )
