

# test_config_parser.py

import unittest
from config_parser import (
    process_input,
    evaluate_expression,
    parse_dict,
    parse_array,
    split_tokens,
    ConfigParserError
)

class TestSplitTokens(unittest.TestCase):
    def test_simple_split(self):
        s = "a, b, c"
        expected = ["a", "b", "c"]
        self.assertEqual(split_tokens(s, ','), expected)

    def test_nested_structures(self):
        s = "dict(name = 'value', list = ({1, 2, 3})), another = 'test'"
        expected = ["dict(name = 'value', list = ({1, 2, 3}))", "another = 'test'"]
        self.assertEqual(split_tokens(s, ','), expected)

    def test_no_delimiter(self):
        s = "single_token"
        expected = ["single_token"]
        self.assertEqual(split_tokens(s, ','), expected)

    def test_empty_string(self):
        s = ""
        expected = []
        self.assertEqual(split_tokens(s, ','), expected)

    def test_complex_nested(self):
        s = "a, dict(b, c), ({d, e, dict(f, g)}), h"
        expected = ["a", "dict(b, c)", "({d, e, dict(f, g)})", "h"]
        self.assertEqual(split_tokens(s, ','), expected)


class TestEvaluateExpression(unittest.TestCase):
    def setUp(self):
        self.variables = {
            "host": {"name": "db.local", "port": 5432},
            "default_user": {"username": "admin", "roles": ["admin", "user"]}
        }

    def test_evaluate_number(self):
        self.assertEqual(evaluate_expression("123", self.variables), 123)
        self.assertEqual(evaluate_expression("-45", self.variables), -45)
        self.assertEqual(evaluate_expression("3.14", self.variables), 3.14)

    def test_evaluate_string(self):
        self.assertEqual(evaluate_expression('"hello"', self.variables), "hello")
        self.assertEqual(evaluate_expression("'world'", self.variables), "world")

    def test_evaluate_variable(self):
        self.assertEqual(evaluate_expression("![host]", self.variables), {"name": "db.local", "port": 5432})
        self.assertEqual(evaluate_expression("![default_user]", self.variables), {"username": "admin", "roles": ["admin", "user"]})

    def test_evaluate_dict(self):
        expr = "dict(name = 'test', value = 10)"
        expected = {"name": "test", "value": 10}
        self.assertEqual(evaluate_expression(expr, self.variables), expected)

    def test_evaluate_array(self):
        expr = "({1, 2, 3})"
        expected = [1, 2, 3]
        self.assertEqual(evaluate_expression(expr, self.variables), expected)

    def test_evaluate_invalid_expression(self):
        with self.assertRaises(ConfigParserError):
            evaluate_expression("invalid_expression", self.variables)

    def test_evaluate_undefined_variable(self):
        with self.assertRaises(ConfigParserError):
            evaluate_expression("![undefined_var]", self.variables)


class TestParseDict(unittest.TestCase):
    def setUp(self):
        self.variables = {
            "host": {"name": "db.local", "port": 5432}
        }

    def test_parse_simple_dict(self):
        dict_content = "name = 'test', value = 10"
        expected = {"name": "test", "value": 10}
        self.assertEqual(parse_dict(dict_content, self.variables), expected)

    def test_parse_nested_dict(self):
        dict_content = "host = ![host], enabled = 1"
        expected = {"host": {"name": "db.local", "port": 5432}, "enabled": 1}
        self.assertEqual(parse_dict(dict_content, self.variables), expected)

    def test_parse_dict_with_array(self):
        dict_content = "roles = ({'admin', 'user'})"
        expected = {"roles": ["admin", "user"]}
        self.assertEqual(parse_dict(dict_content, self.variables), expected)

    def test_parse_dict_invalid_syntax(self):
        dict_content = "name 'test', value = 10"  # Missing '='
        with self.assertRaises(ConfigParserError):
            parse_dict(dict_content, self.variables)

    def test_parse_dict_invalid_key(self):
        dict_content = "123name = 'test'"  # Invalid key
        with self.assertRaises(ConfigParserError):
            parse_dict(dict_content, self.variables)


class TestParseArray(unittest.TestCase):
    def setUp(self):
        self.variables = {
            "host": {"name": "db.local", "port": 5432},
            "default_user": {"username": "admin", "roles": ["admin", "user"]}
        }

    def test_parse_simple_array(self):
        array_content = "1, 2, 3"
        expected = [1, 2, 3]
        self.assertEqual(parse_array(array_content, self.variables), expected)

    def test_parse_array_with_variables(self):
        array_content = "![host], ![host]"
        expected = [{"name": "db.local", "port": 5432}, {"name": "db.local", "port": 5432}]
        self.assertEqual(parse_array(array_content, self.variables), expected)

    def test_parse_array_with_dict(self):
        array_content = "dict(name = 'remote', port = 5433)"
        expected = [{"name": "remote", "port": 5433}]
        self.assertEqual(parse_array(array_content, self.variables), [{"name": "remote", "port": 5433}])

    def test_parse_array_nested(self):
        array_content = "![default_user], dict(username = 'guest', roles = ({'user'}))"
        expected = [
            {"username": "admin", "roles": ["admin", "user"]},
            {"username": "guest", "roles": ["user"]}
        ]
        self.assertEqual(parse_array(array_content, self.variables), expected)

    def test_parse_array_invalid_expression(self):
        array_content = "invalid_expression"
        with self.assertRaises(ConfigParserError):
            parse_array(array_content, self.variables)


class TestProcessInput(unittest.TestCase):
    def test_process_simple_input(self):
        input_text = """
        -- Simple configuration
        var host := "misha";
        """
        expected = {"host": "misha"}
        self.assertEqual(process_input(input_text), expected)

    def test_process_input_with_dict_and_array(self):
        input_text = """
        -- Database configuration
        var host := dict(
            name = "db.local",
            port = 5432
        );
        connections := ({ ![host], ![host], dict(name = "db.remote", port = 5433) });
        """
        expected = {
            "host": {"name": "db.local", "port": 5432},
            "connections": [
                {"name": "db.local", "port": 5432},
                {"name": "db.local", "port": 5432},
                {"name": "db.remote", "port": 5433}
            ]
        }
        self.assertEqual(process_input(input_text), expected)

    def test_process_input_with_multiple_variables(self):
        input_text = """
        -- Application configuration
        var default_user := dict(
            username = "admin",
            roles = ({ "admin", "user" })
        );
        users := ({ ![default_user], dict(username = "guest", roles = ({ "user" })) });
        settings := dict(
            debug = 1,
            paths = ({ "/home", "/var" })
        );
        """
        expected = {
            "default_user": {"username": "admin", "roles": ["admin", "user"]},
            "users": [
                {"username": "admin", "roles": ["admin", "user"]},
                {"username": "guest", "roles": ["user"]}
            ],
            "settings": {
                "debug": 1,
                "paths": ["/home", "/var"]
            }
        }
        self.assertEqual(process_input(input_text), expected)

    def test_process_input_with_invalid_variable_declaration(self):
        input_text = """
        var 123host := "invalid";
        """
        with self.assertRaises(ConfigParserError):
            process_input(input_text)

    def test_process_input_with_redeclared_variable(self):
        input_text = """
        var host := "first";
        var host := "second";
        """
        with self.assertRaises(ConfigParserError):
            process_input(input_text)

    def test_process_input_with_undefined_variable_reference(self):
        input_text = """
        connections := ({ ![undefined_var] });
        """
        with self.assertRaises(ConfigParserError):
            process_input(input_text)

    def test_process_input_with_nested_structures(self):
        input_text = """
        var user := dict(
            name = "Alice",
            attributes = dict(
                age = 30,
                skills = ({ "Python", "Data Science" })
            )
        );
        profile := ![user];
        """
        expected = {
            "user": {
                "name": "Alice",
                "attributes": {
                    "age": 30,
                    "skills": ["Python", "Data Science"]
                }
            },
            "profile": {
                "name": "Alice",
                "attributes": {
                    "age": 30,
                    "skills": ["Python", "Data Science"]
                }
            }
        }
        self.assertEqual(process_input(input_text), expected)


if __name__ == '__main__':
    unittest.main()

