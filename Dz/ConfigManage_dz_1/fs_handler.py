import zipfile


def load_filesystem(zip_path):
    filesystem = {}

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if not file.endswith('/'):
                try:
                    filesystem[file] = zip_ref.read(file).decode('utf-8')
                except UnicodeDecodeError as e:
                    filesystem[file] = zip_ref.read(file)
            else:
                filesystem[file] = None

    return filesystem