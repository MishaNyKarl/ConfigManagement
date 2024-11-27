import os
import subprocess
from typing import List, Dict

def sanitize_name(name: str) -> str:
    return name.replace(":", "_").replace(".", "_").replace("-", "_")


def fetch_dependencies(package_name: str, repository_url: str) -> Dict[str, List[str]]:
    # Анализируем зависимости
    command = ["mvn.cmd", "dependency:tree", "-DoutputType=dot", "-DoutputFile=temp.dot",
               f"-DrepositoryUrl={repository_url}"]

    subprocess.run(command, check=True)

    dependencies = {}
    with open("temp.dot", "r") as file:
        for line in file:
            if "->" in line:
                parent, child = line.strip().split("->")
                parent = sanitize_name(parent.strip())
                child = sanitize_name(child.strip())
                if parent not in dependencies:
                    dependencies[parent] = []
                dependencies[parent].append(child)

    # Удаляем временные файлы
    os.remove("temp.dot")
    return dependencies
