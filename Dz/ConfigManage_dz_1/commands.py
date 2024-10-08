import os


def ls(current_path, filesystem):
    # Проверяем файлы и каталоги в текущем пути

    if current_path == '/':
        current_path = 'filesystem/'

    if not current_path.endswith('/'):
        current_path += '/'

    # Список содержимого текущего каталога
    contents = []
    for path in filesystem.keys():
        if path.startswith(current_path) and path != current_path:
            # Получаем элемент, следующий за текущим путем
            relative_path = path[len(current_path):].split('/')[0]
            if relative_path not in contents:
                contents.append(relative_path)

    # Если в директории ничего нет
    if contents:
        for item in contents:
            print(item)
    else:
        print(f"{current_path}: directory is empty")


def cd(target_path, current_path, filesystem,  home_directory="filesystem/"):
    if current_path == '/':
        current_path = 'filesystem/'

    if target_path == '~':
        return home_directory

        # Если пользователь ввел команду для перехода в родительскую директорию
    if target_path == '..':
        # Если уже находимся в корне файловой системы, то не переходим выше
        if current_path == home_directory:
            return home_directory
        else:
            # Возвращаем путь к родительской директории
            new_path = os.path.dirname(current_path.rstrip('/')) + '/'
            return new_path

        # Проверка абсолютного пути
    if target_path.startswith('/'):
        target_path = 'filesystem' + target_path  # Преобразуем абсолютный путь

        # Создаем полный путь для навигации
    new_path = os.path.join(current_path, target_path)
    # Проверяем, что новый путь существует и является директорией
    if new_path in filesystem or new_path + '/' in filesystem:
        if '.' in new_path:
            print(f'cd: {target_path} is not a directory')
            return None
        # Если директория существует, возвращаем новый путь
        return new_path + '/' if not new_path.endswith('/') else new_path
    else:
        print(f"cd: no such directory: {target_path}")
        return None


def rev(filename, current_path, filesystem):

    current_path = os.path.join(current_path + filename)

    for file in filesystem:
        if file.startswith(current_path):
            try:
                content = filesystem[file]
                print(content[::-1])
                return
            except UnicodeDecodeError:
                try:
                    # Если UTF-8 не работает, пробуем как UTF-16LE
                    decoded_content = filesystem[file].decode('utf-16le')
                    print(decoded_content[::-1])
                    return
                except UnicodeDecodeError:
                    print(f"rev: {file}: cannot decode file (unknown encoding)")
                    return

    print(f"rev: {filename}: No such file")



def du(file_search, current_path, filesystem):
    total_size = 0

    current_path = os.path.join(current_path, file_search)

    if current_path not in filesystem and current_path + '/' not in filesystem:
        print(f"du: {file_search}: No such file or directory")
        return

    for file in filesystem:
        if file.startswith(current_path):
            if filesystem[file] is not None:  # Только файлы имеют размер
                total_size += len(filesystem[file])

    print(f"Total size: {total_size} bytes")




