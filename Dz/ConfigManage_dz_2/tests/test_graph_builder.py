import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from graph_builder import build_graph

class TestGraphBuilder(unittest.TestCase):
    @unittest.mock.patch("graphviz.Digraph.render")
    def test_build_graph(self, mock_render):
        dependencies = {"A": ["B"], "B": ["C"]}
        build_graph(dependencies, output_file="test_graph")
        mock_render.assert_called_once_with("test_graph", view=True)
