import unittest
from unittest.mock import patch
from emulator import parse_arguments
import os
import xml.etree.ElementTree as ET
from logger import log_action
from fs_handler import load_filesystem
import zipfile


class TestParseArguments(unittest.TestCase):

    @patch('sys.argv', ['emulator.py', '--user', 'Misha', '--host', 'Desctop123', '--zipfile', 'filesystem.zip', '--logfile', 'logfile.xml'])
    def test_parse_arguments(self):
        args = parse_arguments()
        self.assertEqual(args.user, 'Misha')
        self.assertEqual(args.host, 'Desctop123')
        self.assertEqual(args.zipfile, 'filesystem.zip')
        self.assertEqual(args.logfile, 'logfile.xml')


class TestLogAction(unittest.TestCase):

    def setUp(self):
        # Создаем временный лог-файл
        self.logfile = 'test_logfile.xml'
        open(self.logfile, 'w').close()  # Создаем пустой файл

    def tearDown(self):
        # Удаляем временный лог-файл после тестов
        if os.path.exists(self.logfile):
            os.remove(self.logfile)

    def test_log_action(self):
        # Логируем команду
        log_action('Misha', 'ls', self.logfile)

        # Проверяем содержимое XML-файла
        tree = ET.parse(self.logfile)
        root = tree.getroot()

        self.assertEqual(root.tag, 'log')
        entry = root.find('entry')
        self.assertIsNotNone(entry)

        user = entry.find('user').text
        command = entry.find('command').text

        self.assertEqual(user, 'Misha')
        self.assertEqual(command, 'ls')


class TestLoadFilesystem(unittest.TestCase):

    def setUp(self):
        # Создаем временный zip-файл для тестов
        self.zipfile = 'test_filesystem.zip'
        with zipfile.ZipFile(self.zipfile, 'w') as zf:
            zf.writestr('file1.txt', 'Content of file 1')
            zf.writestr('dir1/file2.txt', 'Content of file 2')

    def tearDown(self):
        # Удаляем временный zip-файл после тестов
        if os.path.exists(self.zipfile):
            os.remove(self.zipfile)

    def test_load_filesystem(self):
        # Загружаем файловую систему
        filesystem = load_filesystem(self.zipfile)

        # Проверяем, что файлы были корректно загружены
        self.assertIn('file1.txt', filesystem)
        self.assertIn('dir1/file2.txt', filesystem)

        # Сравниваем содержимое файлов напрямую (без декодирования)
        self.assertEqual(filesystem['file1.txt'], 'Content of file 1')
        self.assertEqual(filesystem['dir1/file2.txt'], 'Content of file 2')


if __name__ == '__main__':
    unittest.main()

