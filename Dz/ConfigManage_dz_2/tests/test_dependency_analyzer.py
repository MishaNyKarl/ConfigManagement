import unittest
from unittest.mock import patch, mock_open
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from dependency_analyzer import fetch_dependencies

class TestDependencyAnalyzer(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="A -> B\nB -> C\n")
    @patch("os.remove")
    @patch("subprocess.run")
    def test_fetch_dependencies(self, mock_subprocess, mock_remove, mock_file):
        dependencies = fetch_dependencies("example-package", "http://example.com")
        self.assertEqual(dependencies, {"A": ["B"], "B": ["C"]})
