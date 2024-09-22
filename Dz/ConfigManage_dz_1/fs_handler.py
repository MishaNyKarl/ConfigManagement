import zipfile


def load_filesystem(zip_path):
    filesystem = {}

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if not file.endswith('/'):
                try:
                    # Попробуем декодировать файл как текст (UTF-8)
                    filesystem[file] = zip_ref.read(file).decode('utf-8')
                except UnicodeDecodeError as e:
                    # Если файл нельзя декодировать, сохраняем его как бинарные данные
                    filesystem[file] = zip_ref.read(file)
            else:
                # Если это директория, добавляем её как ключ в словарь, но без содержимого
                filesystem[file] = None

    return filesystem