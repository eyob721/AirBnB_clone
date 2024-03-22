#!/usr/bin/python3
"""Tests for the AirBnB clone - console"""
import os
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from console import HBNBCommand
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


def get_cmd_output(command: str):
    """Returns the output string from stdout of a console command"""
    with patch("sys.stdout", new=StringIO()) as output:
        HBNBCommand().onecmd(command)
        return output.getvalue()


valid_classes = (
    "Amenity",
    "BaseModel",
    "City",
    "Place",
    "Review",
    "State",
    "User",
)


class TestHBNBCommand(TestCase):
    """Tests for the console"""

    def test_prompt(self):
        """Check the prompt of the console"""
        self.assertEqual(HBNBCommand.prompt, "(hbnb) ")

    def test_emptyline(self):
        """Check emptyline + ENTER"""
        output_exp = ""

        output_got = get_cmd_output("")
        self.assertEqual(output_exp, output_got)

        output_got = get_cmd_output("   \n\n\n")
        self.assertEqual(output_exp, output_got)

    def test_quit(self):
        """Check exiting the console using the quit command"""
        self.assertEqual(HBNBCommand().onecmd("quit"), True)

        output_exp = ""
        output_got = get_cmd_output("quit")
        self.assertEqual(output_got, output_exp)

    def test_EOF(self):
        """Check exiting the command using EOF"""
        self.assertEqual(HBNBCommand().onecmd("EOF"), True)

        output_exp = "\n"
        output_got = get_cmd_output("EOF")
        self.assertEqual(output_got, output_exp)


class TestHBNBCommandCreate(TestCase):
    """Tests for the create command"""

    def test_create_missing_class_name(self):
        """create - missing class name"""
        output_exp = "** class name missing **\n"
        output_got = get_cmd_output("create")
        self.assertEqual(output_got, output_exp)

    def test_create_invalid_class_name(self):
        """create - invalid class name"""
        output_exp = "** class doesn't exist **\n"
        output_got = get_cmd_output("create MyModel")
        self.assertEqual(output_got, output_exp)

    def test_create_correct_usage(self):
        """create - valid class name"""
        output_exp = r"^\w+-\w+-\w+-\w+-\w+$\n"
        # TODO: add more classes later on
        for cls in valid_classes:
            output_got = get_cmd_output(f"create {cls}")
            # Check id output
            self.assertRegex(output_got, output_exp)
            # Check that instance is actuall created
            key = "{}.{}".format(cls, output_got.rstrip("\n"))
            self.assertIn(key, storage.all())


class TestHBNBCommandShow(TestCase):
    """Tests for the show command"""

    def test_show_missing_class_name(self):
        """show - missing class name"""
        output_exp = "** class name missing **\n"
        output_got = get_cmd_output("show")
        self.assertEqual(output_got, output_exp)

    def test_show_invalid_class_name(self):
        """show - invalid class name"""
        output_exp = "** class doesn't exist **\n"
        output_got = get_cmd_output("show MyModel")
        self.assertEqual(output_got, output_exp)

    def test_show_missing_id(self):
        """show - missing id"""
        output_exp = "** instance id missing **\n"
        output_got = get_cmd_output("show BaseModel")
        self.assertEqual(output_got, output_exp)

    def test_show_missing_instance(self):
        """show - invalid id"""
        output_exp = "** no instance found **\n"
        output_got = get_cmd_output("show BaseModel 123")
        self.assertEqual(output_got, output_exp)

    def test_show_correct_usage(self):
        """show - valid class name and id"""
        for cls in valid_classes:
            obj = eval("{}()".format(cls))
            output_exp = str(obj) + "\n"
            output_got = get_cmd_output(f"show {cls} {obj.id}")
            self.assertEqual(output_got, output_exp)

    def test_show_correct_usage_with_extra_arguments(self):
        """show - valid class name and id, but with extra arguments"""
        # extra arguments should be ignored
        for cls in valid_classes:
            obj = eval("{}()".format(cls))
            output_exp = str(obj) + "\n"
            output_got = get_cmd_output(f"show {cls} {obj.id} extra args")
            self.assertEqual(output_got, output_exp)


class HBNBCommandDestroy(TestCase):
    """Tests for the destroy command"""

    def test_destroy_missing_class_name(self):
        """destroy - missing class name"""
        output_exp = "** class name missing **\n"
        output_got = get_cmd_output("destroy")
        self.assertEqual(output_got, output_exp)

    def test_destroy_invalid_class_name(self):
        """destroy - invalid class name"""
        output_exp = "** class doesn't exist **\n"
        output_got = get_cmd_output("destroy MyModel")
        self.assertEqual(output_got, output_exp)

    def test_destroy_missing_id(self):
        """destroy - missing id"""
        output_exp = "** instance id missing **\n"
        output_got = get_cmd_output("destroy BaseModel")
        self.assertEqual(output_got, output_exp)

    def test_destroy_missing_instance(self):
        """destroy - invalid id"""
        output_exp = "** no instance found **\n"
        output_got = get_cmd_output("destroy BaseModel 123")
        self.assertEqual(output_got, output_exp)

    def test_destroy_correct_usage(self):
        """destroy - valid class name and id"""
        for cls in valid_classes:
            obj = eval("{}()".format(cls))
            key = f"{cls}.{obj.id}"
            HBNBCommand().onecmd(f"destroy {cls} {obj.id}")
            self.assertNotIn(key, storage.all().keys())

    def test_destroy_correct_usage_with_extra_arguments(self):
        """destroy - valid class name and id, but with extra arguments"""
        # extra arguments should be ignored
        for cls in valid_classes:
            obj = eval("{}()".format(cls))
            key = f"{cls}.{obj.id}"
            HBNBCommand().onecmd(f"destroy {cls} {obj.id} extra args")
            self.assertNotIn(key, storage.all().keys())


class HBNBCommandAll(TestCase):
    """Tests for the all command"""

    def test_all_invalid_class_name(self):
        """all - invalid class name"""
        output_exp = "** class doesn't exist **\n"
        output_got = get_cmd_output("all MyModel")
        self.assertEqual(output_got, output_exp)

    def test_all_without_class_name(self):
        """all - no class name"""
        obj_list = [str(obj) for obj in storage.all().values()]
        output_exp = "" if obj_list == [] else str(obj_list) + "\n"
        output_got = get_cmd_output("all")
        self.assertEqual(output_got, output_exp)

    def test_all_with_class_name(self):
        """all - valid class name"""
        for cls in valid_classes:
            obj_list = [
                str(obj)
                for obj in storage.all().values()
                if type(obj).__name__ == cls
            ]
            output_exp = "" if obj_list == [] else str(obj_list) + "\n"
            output_got = get_cmd_output(f"all {cls}")
            self.assertEqual(output_got, output_exp)


class TestHBNBCommandUpdate(TestCase):
    """Tests for the update command"""

    def test_update_missing_class_name(self):
        """update - missing class name"""
        output_exp = "** class name missing **\n"
        output_got = get_cmd_output("update")
        self.assertEqual(output_got, output_exp)

    def test_update_invalid_class_name(self):
        """update - invalid class name"""
        output_exp = "** class doesn't exist **\n"
        output_got = get_cmd_output("update MyModel")
        self.assertEqual(output_got, output_exp)

    def test_update_missing_id(self):
        """update - missing id"""
        output_exp = "** instance id missing **\n"
        output_got = get_cmd_output("update BaseModel")
        self.assertEqual(output_got, output_exp)

    def test_update_missing_instance(self):
        """update - invalid id"""
        output_exp = "** no instance found **\n"
        output_got = get_cmd_output("update BaseModel 123")
        self.assertEqual(output_got, output_exp)

    def test_update_missing_attribute(self):
        """update - missing attribute name"""
        b = BaseModel()
        output_exp = "** attribute name missing **\n"
        output_got = get_cmd_output(f"update BaseModel {b.id}")
        self.assertEqual(output_got, output_exp)

    def test_update_missing_value(self):
        """update - missing value"""
        b = BaseModel()
        output_exp = "** value missing **\n"
        output_got = get_cmd_output(f"update BaseModel {b.id} eg")
        self.assertEqual(output_got, output_exp)

    def test_update_correct_usages(self):
        """update - valid class, id, attribute and value"""
        for cls in valid_classes:
            obj = eval("{}()".format(cls))

            cases = {
                "name": '"John Doe"',
                "gender": "M",
                "age": 47,
                "height": 1.82,
                "email": '"john@gmail.com"',
            }

            for attr in cases.keys():
                HBNBCommand().onecmd(
                    "update {} {} {} {}".format(cls, obj.id, attr, cases[attr])
                )
                # Check that attribute is set
                self.assertIn(attr, obj.to_dict())
                if type(cases[attr]) is str:
                    self.assertEqual(
                        getattr(obj, attr), cases[attr].strip("\"'")
                    )
                else:
                    self.assertEqual(getattr(obj, attr), cases[attr])
                # Check that attribute value is properly casted
                self.assertIs(type(getattr(obj, attr)), type(cases[attr]))

            # Check that it is saved
            storage.reload()
            key = f"{cls}.{obj.id}"
            obj = storage.all()[key]
            obj_dict = obj.to_dict()

            for attr in cases:
                self.assertIn(attr, obj_dict)
                if type(cases[attr]) is str:
                    self.assertEqual(
                        getattr(obj, attr), cases[attr].strip("\"'")
                    )
                else:
                    self.assertEqual(getattr(obj, attr), cases[attr])
                # Check that attribute value is properly casted
                self.assertIs(type(getattr(obj, attr)), type(cases[attr]))

    def test_update_correct_usage_with_extra_args(self):
        """update - valid class, id, attribute and value but with extra args"""
        for cls in valid_classes:
            obj = eval("{}()".format(cls))

            HBNBCommand().onecmd(
                f"update {cls} {obj.id} name 'John Doe' this is extra "
            )
            self.assertIn("name", obj.to_dict())
            self.assertEqual(getattr(obj, "name"), "John Doe")
            self.assertIs(type(getattr(obj, "name")), str)

            HBNBCommand().onecmd(f"update {cls} {obj.id} age 47 this is extra")
            self.assertIn("age", obj.to_dict())
            self.assertEqual(getattr(obj, "age"), 47)
            self.assertIs(type(getattr(obj, "age")), int)

            HBNBCommand().onecmd(
                f"update {cls} {obj.id} height 3.14 this is extra"
            )
            self.assertIn("height", obj.to_dict())
            self.assertEqual(getattr(obj, "height"), 3.14)
            self.assertIs(type(getattr(obj, "height")), float)


class TestHBNBCommandHelps(TestCase):
    """Tests for the helps sections of the console"""

    def test_help(self):
        """help"""
        output_exp = """
Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

"""
        output_got = get_cmd_output("help")
        self.assertEqual(output_got, output_exp)

    def test_help_quit(self):
        """help quit"""
        output_exp = "Usage: quit\n" + "Quits from the console.\n"
        output_got = get_cmd_output("help quit")
        self.assertEqual(output_got, output_exp)

    def test_help_EOF(self):
        """help EOF"""
        output_exp = (
            "Usage: EOF\n" + "Handles end-of-file signal. Exits the program.\n"
        )
        output_got = get_cmd_output("help EOF")
        self.assertEqual(output_got, output_exp)

    def test_help_create(self):
        """help create"""
        output_exp = (
            "Usage: create <class name>\n"
            + "Creates a new instance of the given class name, saves it to the"
            + " JSON file and prints the id.\n"
        )
        output_got = get_cmd_output("help create")
        self.assertEqual(output_got, output_exp)

    def test_help_show(self):
        """help show"""
        output_exp = (
            "Usage: show <class name> <id>\n"
            + "Prints the string representation of an instance, based on the "
            + "class name and id.\n"
        )
        output_got = get_cmd_output("help show")
        self.assertEqual(output_got, output_exp)

    def test_help_destroy(self):
        """help destroy"""
        output_exp = (
            "Usage: destroy <class name> <id>\n"
            + "Destroys an instance based on the class name and id, and saves "
            + "the change into the JSON file.\n"
        )
        output_got = get_cmd_output("help destroy")
        self.assertEqual(output_got, output_exp)

    def test_help_all(self):
        """help all"""
        output_exp = (
            "Usage: all [class name]\n"
            + "Prints the string representation of all instances.\n"
            + "With class name, then only string representation of instances "
            + "with that class will be printed.\n"
        )
        output_got = get_cmd_output("help all")
        self.assertEqual(output_got, output_exp)

    def test_help_update(self):
        """help update"""
        output_exp = (
            "Usage: update <class name> <id> <attribute name> <value>\n"
            + "Updates an instance based on the class name and id by "
            + "adding or updating an attribute.\n"
            + "The change is saved to the JSON file."
            + "The value is type casted when it is assigned and "
            + "all extra arguments are ignored.\n"
        )
        output_got = get_cmd_output("help update")
        self.assertEqual(output_got, output_exp)


class HBNBCommandAllAdvanced(TestCase):
    """Tests for <class name>.all() command"""

    def test_all_invalid_class_name(self):
        """<class name>.all() - invalid class name"""
        output_exp = "** class doesn't exist **\n"
        output_got = get_cmd_output("MyModel.all()")
        self.assertEqual(output_got, output_exp)

    def test_all_with_class_name(self):
        """<class name>.all() - valid class name"""
        for cls in valid_classes:
            obj_list = [
                str(obj)
                for obj in storage.all().values()
                if type(obj).__name__ == cls
            ]
            output_exp = "" if obj_list == [] else str(obj_list) + "\n"
            output_got = get_cmd_output(f"{cls}.all()")
            self.assertEqual(output_got, output_exp)


class HBNBCommandCountAdvanced(TestCase):
    """Tests for the <class name>.count() command"""

    def test_count(self):
        """<class name>.count()"""
        classes = (
            "MyModel",
            "Amenity",
            "BaseModel",
            "City",
            "Place",
            "Review",
            "State",
            "User",
        )

        for cls in classes:
            count = [
                type(obj).__name__ for obj in storage.all().values()
            ].count(cls)
            output_exp = str(count) + "\n"
            output_got = get_cmd_output(f"{cls}.count()")
            self.assertEqual(output_got, output_exp)


class TestHBNBCommandShowAdvance(TestCase):
    """Tests for the <class name>.show(<id>) command"""

    def test_show_invalid_class_name(self):
        """<class name>.show(<id>) - invalid class name"""
        output_exp = "** class doesn't exist **\n"
        output_got = get_cmd_output("MyModel.show()")
        self.assertEqual(output_got, output_exp)

    def test_show_missing_id(self):
        """<class name>.show(<id>) - missing id"""
        output_exp = "** instance id missing **\n"
        output_got = get_cmd_output("BaseModel.show()")
        self.assertEqual(output_got, output_exp)

    def test_show_missing_instance(self):
        """<class name>.show(<id>) - invalid id"""
        output_exp = "** no instance found **\n"
        output_got = get_cmd_output("BaseModel.show(123)")
        self.assertEqual(output_got, output_exp)

    def test_show_correct_usage(self):
        """<class name>.show(<id>) - valid class name and id"""
        for cls in valid_classes:
            obj = eval("{}()".format(cls))
            output_exp = str(obj) + "\n"
            output_got = get_cmd_output(f"{cls}.show({obj.id})")
            self.assertEqual(output_got, output_exp)

    def test_show_correct_usage_with_extra_arguments(self):
        """<class name>.show(<id>) - valid class and id, but with extra args"""
        # extra arguments should be ignored
        for cls in valid_classes:
            obj = eval("{}()".format(cls))
            output_exp = str(obj) + "\n"
            output_got = get_cmd_output(f"{cls}.show({obj.id}, extra, args)")
            self.assertEqual(output_got, output_exp)


class TestHBNBCommandDestroyAdvance(TestCase):
    """Tests for the <class name>.destroy(<id>) command"""

    def test_destroy_invalid_class_name(self):
        """<class name>.destroy(<id>) - invalid class name"""
        output_exp = "** class doesn't exist **\n"
        output_got = get_cmd_output("MyModel.destroy()")
        self.assertEqual(output_got, output_exp)

    def test_destroy_missing_id(self):
        """<class name>.destroy(<id>) - missing id"""
        output_exp = "** instance id missing **\n"
        output_got = get_cmd_output("BaseModel.destroy()")
        self.assertEqual(output_got, output_exp)

    def test_destroy_missing_instance(self):
        """<class name>.destroy(<id>) - invalid id"""
        output_exp = "** no instance found **\n"
        output_got = get_cmd_output("BaseModel.destroy(123)")
        self.assertEqual(output_got, output_exp)

    def test_destroy_correct_usage(self):
        """<class name>.destroy(<id>) - valid class name and id"""
        for cls in valid_classes:
            obj = eval("{}()".format(cls))
            key = f"{cls}.{obj.id}"
            HBNBCommand().onecmd(f"{cls}.destroy({obj.id})")
            self.assertNotIn(key, storage.all().keys())

    def test_destroy_correct_usage_with_extra_arguments(self):
        """<class name>.destroy(<id>) - valid class and id, with extra args"""
        # extra arguments should be ignored
        for cls in valid_classes:
            obj = eval("{}()".format(cls))
            key = f"{cls}.{obj.id}"
            HBNBCommand().onecmd(f"{cls}.destroy({obj.id}, extra, args)")
            self.assertNotIn(key, storage.all().keys())


class TestHBNBCommandUpdateAdvanced(TestCase):
    """Tests for the <class name>.update(<id>, <attr>, <value>) command"""

    def test_update_invalid_class_name(self):
        """<class name>.update(<id>, <attr>, <value>) - invalid class name"""
        output_exp = "** class doesn't exist **\n"
        output_got = get_cmd_output("MyModel.update()")
        self.assertEqual(output_got, output_exp)

    def test_update_missing_id(self):
        """<class name>.update(<id>, <attr>, <value>) - missing id"""
        output_exp = "** instance id missing **\n"
        output_got = get_cmd_output("BaseModel.update()")
        self.assertEqual(output_got, output_exp)

    def test_update_missing_instance(self):
        """<class name>.update(<id>, <attr>, <value>) - invalid id"""
        output_exp = "** no instance found **\n"
        output_got = get_cmd_output("BaseModel.update(123)")
        self.assertEqual(output_got, output_exp)

    def test_update_missing_attribute(self):
        """<class name>.update(<id>, <attr>, <value>) - missing attribute"""
        b = BaseModel()
        output_exp = "** attribute name missing **\n"
        output_got = get_cmd_output(f"BaseModel.update({b.id})")
        self.assertEqual(output_got, output_exp)

    def test_update_missing_value(self):
        """<class name>.update(<id>, <attr>, <value>) - missing value"""
        b = BaseModel()
        output_exp = "** value missing **\n"
        output_got = get_cmd_output(f"BaseModel.update({b.id}, eg)")
        self.assertEqual(output_got, output_exp)

    def test_update_correct_usages(self):
        """<class name>.update(<id>, <attr>, <value>) - valid args"""
        for cls in valid_classes:
            obj = eval("{}()".format(cls))

            cases = {
                "name": '"John Doe"',
                "gender": "M",
                "age": 47,
                "height": 1.82,
                "email": '"john@gmail.com"',
            }

            for attr in cases.keys():
                HBNBCommand().onecmd(
                    "{}.update({}, {}, {})".format(
                        cls, obj.id, attr, cases[attr]
                    )
                )
                # Check that attribute is set
                self.assertIn(attr, obj.to_dict())
                if type(cases[attr]) is str:
                    self.assertEqual(
                        getattr(obj, attr), cases[attr].strip("\"'")
                    )
                else:
                    self.assertEqual(getattr(obj, attr), cases[attr])
                # Check that attribute value is properly casted
                self.assertIs(type(getattr(obj, attr)), type(cases[attr]))

            # Check that it is saved
            storage.reload()
            key = f"{cls}.{obj.id}"
            obj = storage.all()[key]
            obj_dict = obj.to_dict()

            for attr in cases:
                self.assertIn(attr, obj_dict)
                if type(cases[attr]) is str:
                    self.assertEqual(
                        getattr(obj, attr), cases[attr].strip("\"'")
                    )
                else:
                    self.assertEqual(getattr(obj, attr), cases[attr])
                # Check that attribute value is properly casted
                self.assertIs(type(getattr(obj, attr)), type(cases[attr]))

    def test_update_correct_usage_with_extra_args(self):
        """<class name>.update(<id>, <attr>, <value>) - with extra args"""
        for cls in valid_classes:
            obj = eval("{}()".format(cls))

            HBNBCommand().onecmd(
                f"{cls}.update({obj.id}, name, 'John Doe', this is extra )"
            )
            self.assertIn("name", obj.to_dict())
            self.assertEqual(getattr(obj, "name"), "John Doe")
            self.assertIs(type(getattr(obj, "name")), str)

            HBNBCommand().onecmd(
                f"{cls}.update({obj.id}, age, 47, this is extra)"
            )
            self.assertIn("age", obj.to_dict())
            self.assertEqual(getattr(obj, "age"), 47)
            self.assertIs(type(getattr(obj, "age")), int)

            HBNBCommand().onecmd(
                f"{cls}.update({obj.id}, height, 3.14, this is extra)"
            )
            self.assertIn("height", obj.to_dict())
            self.assertEqual(getattr(obj, "height"), 3.14)
            self.assertIs(type(getattr(obj, "height")), float)


class TestHBNBCommandUpdateAdvancedDictionary(TestCase):
    """Tests for the <class name>.update(<id>, <dict>) command"""

    test_dict = {
        "full_name": "John Doe",
        "age": 29,
        "height": 1.78,
        "email": "airbnb@mail.com",
    }

    def test_update_invalid_class_name(self):
        """<class name>.update(<id>, <dict>) - invalid class name"""
        output_exp = "** class doesn't exist **\n" * len(self.test_dict)
        output_got = get_cmd_output(f"MyModel.update({self.test_dict})")
        self.assertEqual(output_got, output_exp)

    def test_update_missing_id(self):
        """<class name>.update(<id>, <dict>) - missing id"""
        output_exp = "** instance id missing **\n" * len(self.test_dict)
        output_got = get_cmd_output(f"BaseModel.update({self.test_dict})")
        self.assertEqual(output_got, output_exp)

    def test_update_missing_instance(self):
        """<class name>.update(<id>, <dict>) - invalid id"""
        output_exp = "** no instance found **\n" * len(self.test_dict)
        output_got = get_cmd_output(f"BaseModel.update(123, {self.test_dict})")
        self.assertEqual(output_got, output_exp)

    def test_update_correct_usages(self):
        """<class name>.update(<id>, <dict>) - valid class, id, and dict"""
        for cls in valid_classes:
            obj = eval("{}()".format(cls))

            HBNBCommand().onecmd(f"{cls}.update({obj.id}, {self.test_dict})")

            for attr in self.test_dict:
                # Check that attribute is set
                self.assertIn(attr, obj.to_dict())

                # Check value is properly assigned
                if type(self.test_dict[attr]) is str:
                    self.assertEqual(
                        getattr(obj, attr), self.test_dict[attr].strip("\"'")
                    )
                else:
                    self.assertEqual(getattr(obj, attr), self.test_dict[attr])

                # Check that attribute value is properly casted
                self.assertIs(
                    type(getattr(obj, attr)), type(self.test_dict[attr])
                )
