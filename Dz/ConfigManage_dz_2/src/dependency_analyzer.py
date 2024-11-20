import os
import subprocess
from typing import List, Dict

def fetch_dependencies(package_name: str, repository_url: str) -> Dict[str, List[str]]:
    """
    Анализирует зависимости пакета Maven.
    :param package_name: Имя Maven пакета.
    :param repository_url: URL репозитория Maven.
    :return: Словарь с зависимостями {пакет: [зависимости]}.
    """
    # Запускаем Maven для получения зависимостей
    command = [
        "mvn",
        "dependency:tree",
        "-DoutputType=dot",
        "-DoutputFile=temp.dot",
        f"-DrepositoryUrl={repository_url}"
    ]
    subprocess.run(command, check=True)

    # Парсим результат
    dependencies = {}
    with open("temp.dot", "r") as file:
        for line in file:
            if "->" in line:
                parent, child = line.strip().split("->")
                parent = parent.strip()
                child = child.strip()
                if parent not in dependencies:
                    dependencies[parent] = []
                dependencies[parent].append(child)

    # Удаляем временные файлы
    os.remove("temp.dot")
    return dependencies
