import unittest
from io import StringIO
import sys
from commands import ls, cd, du, rev


class TestLSCommand(unittest.TestCase):
    def setUp(self):
        self.filesystem = {
            'filesystem/': None,
            'filesystem/file1.txt': b'File 1 content',
            'filesystem/dir1/': None,
            'filesystem/dir1/file2.txt': b'File 2 content',
            'filesystem/dir2/': None
        }

    def test_ls_non_empty_directory(self):
        captured_output = StringIO()
        sys.stdout = captured_output

        ls('filesystem', self.filesystem)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip().split('\n')

        expected_output = ['dir1', 'dir2', 'file1.txt']
        self.assertCountEqual(output, expected_output)

    def test_ls_empty_directory(self):
        # Перенаправляем вывод
        captured_output = StringIO()
        sys.stdout = captured_output

        # Тестируем ls на пустом каталоге
        ls('filesystem/dir2', self.filesystem)

        # Проверяем, что вывод корректен
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()

        # Ожидаемый вывод: путь к каталогу с сообщением о пустом содержимом
        expected_output = "filesystem/dir2/: directory is empty"
        self.assertEqual(output, expected_output)


class TestCDCommand(unittest.TestCase):
    def setUp(self):
        self.filesystem = {
            'filesystem/': None,
            'filesystem/file1.txt': b'File 1 content',
            'filesystem/dir1/': None,
            'filesystem/dir1/file2.txt': b'File 2 content',
            'filesystem/dir2/': None
        }

    def test_cd_with_not_existing_directory(self):
        captured_output = StringIO()
        sys.stdout = captured_output

        cd('dir14', 'filesystem/', self.filesystem)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()
        expected_output = "cd: no such directory: dir14"
        self.assertEqual(output, expected_output)

    def test_cd_existing_directory(self):
        current_path = 'filesystem/'
        new_path = cd('dir1', current_path, self.filesystem)
        self.assertEqual(new_path, 'filesystem/dir1/')

class TestDUCommand(unittest.TestCase):
    def setUp(self):
        self.filesystem = {
            'filesystem/': None,
            'filesystem/file1.txt': b'File 1 content',
            'filesystem/dir1/': None,
            'filesystem/dir1/file2.txt': b'File 2 content',
            'filesystem/dir2/': None
        }

    def test_du_size_of_existing_directory(self):
        captured_output = StringIO()
        sys.stdout = captured_output

        du('file1.txt', 'filesystem/', self.filesystem)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()
        expected_output = "Total size: 14 bytes"
        self.assertEqual(output, expected_output)

    def test_du_size_of_not_existing_directory(self):
        captured_output = StringIO()
        sys.stdout = captured_output

        du('dir13', 'filesystem/', self.filesystem)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()
        expected_output = "du: dir13: No such file or directory"
        self.assertEqual(output, expected_output)
class TestREVCommand(unittest.TestCase):
    def setUp(self):
        self.filesystem = {
            'filesystem/': None,
            'filesystem/file1.txt': b'File 1 content',
            'filesystem/dir1/': None,
            'filesystem/dir1/file2.txt': b'File 2 content',
            'filesystem/dir2/': None
        }

    def test_rev_on_existing_file(self):
        captured_output = StringIO()
        sys.stdout = captured_output

        rev('file1.txt', 'filesystem/', self.filesystem)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()
        expected_output = "b'tnetnoc 1 eliF'"
        self.assertEqual(output, expected_output)

    def test_rev_on_not_existing_file(self):
        captured_output = StringIO()
        sys.stdout = captured_output

        rev('file3.txt', 'filesystem/', self.filesystem)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()
        expected_output = "rev: file3.txt: No such file"
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()