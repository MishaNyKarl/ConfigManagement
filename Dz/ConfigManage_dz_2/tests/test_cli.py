import argparse
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from cli import main

class TestCLI(unittest.TestCase):
    @patch("argparse.ArgumentParser.parse_args")
    @patch("cli.fetch_dependencies")
    @patch("cli.build_graph")
    def test_main(self, mock_build_graph, mock_fetch_dependencies, mock_parse_args):
        # Настраиваем аргументы командной строки
        mock_parse_args.return_value = argparse.Namespace(
            visualizer="../src/graph_builder.py",
            package="com.example:example-project",
            repository="https://repo.maven.apache.org/maven2"
        )

        # Настраиваем возвращаемое значение для fetch_dependencies
        mock_fetch_dependencies.return_value = {"A": ["B"], "B": ["C"]}

        # Запускаем main
        main()

        # Проверяем, что fetch_dependencies вызван с правильными аргументами
        mock_fetch_dependencies.assert_called_once_with(
            "com.example:example-project",
            "https://repo.maven.apache.org/maven2"
        )

        # Проверяем, что build_graph вызван с правильными данными
        mock_build_graph.assert_called_once_with({"A": ["B"], "B": ["C"]})


if __name__ == "__main__":
    unittest.main()
