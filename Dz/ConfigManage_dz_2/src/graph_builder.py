from graphviz import Digraph


def build_graph(dependencies: dict[str, list[str]], output_file: str = "dependencies") -> None:
    dot = Digraph(format="png")

    for parent, children in dependencies.items():
        for child in children:
            dot.edge(parent, child)

    dot.render(output_file, view=True)
