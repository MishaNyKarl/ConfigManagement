import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import os


def log_action(user, action, logfile):
    # Если файл не существует или пустой, создаем базовую структуру
    if not os.path.exists(logfile) or os.stat(logfile).st_size == 0:
        root = ET.Element("log")
        tree = ET.ElementTree(root)
        with open(logfile, 'wb') as f:
            tree.write(f)

    # Загружаем существующий лог
    tree = ET.parse(logfile)
    root = tree.getroot()

    # Добавляем новую запись в лог
    entry = ET.SubElement(root, "entry")
    time = ET.SubElement(entry, "time")
    time.text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cmd = ET.SubElement(entry, "command")
    cmd.text = action
    usr = ET.SubElement(entry, "user")
    usr.text = user

    # Преобразуем XML в строку с красивым форматированием
    rough_string = ET.tostring(root, 'utf-8')

    # Сохраняем изменения с отступами и переносами строк
    tree.write(logfile)