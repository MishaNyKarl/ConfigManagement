import argparse
from dependency_analyzer import fetch_dependencies
from graph_builder import build_graph


def main():
    parser = argparse.ArgumentParser(description="Maven Dependency Visualizer")
    parser.add_argument("--visualizer", required=True, help="Путь к программе для визуализации графов")
    parser.add_argument("--package", required=True, help="Имя анализируемого пакета")
    parser.add_argument("--repository", required=True, help="URL-адрес репозитория Maven")

    args = parser.parse_args()

    # Анализируем зависимости
    dependencies = fetch_dependencies(args.package, args.repository)

    # Строим граф
    build_graph(dependencies)


if __name__ == "__main__":
    main()
