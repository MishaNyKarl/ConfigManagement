import argparse
from fs_handler import load_filesystem
from commands import ls, cd, rev, du
from logger import log_action
import os
import sys


def parse_arguments():
    parse = argparse.ArgumentParser(description='Shell Emulator')
    parse.add_argument('--user', required=True, help='Имя пользователя')
    parse.add_argument('--host', required=True, help='Имя компьютера')
    parse.add_argument('--zipfile', required=True, help='Путь к zip-архиву файловой системы')
    parse.add_argument('--logfile', required=True, help='Путь к xml лог-файлу')
    return parse.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    print(f"Пользователь: {args.user}, Компьютер: {args.host}, Zip файл: {args.zipfile}, Лог файл: {args.logfile}")

    filesystem = load_filesystem(args.zipfile)
    current_path = 'filesystem/'
    user = args.user
    host = args.host
    open(args.logfile, 'w').close()

    while True:
        # Формирование приглашения к вводу
        prompt = f"{user}@{host}:{current_path}$ "
        command = input(prompt)

        # Логирование команды
        log_action(user, command, args.logfile)

        # Разбиваем команду на имя команды и аргументы
        parts = command.split()
        if len(parts) == 0:
            continue
        cmd = parts[0]
        cmd_args = parts[1:]

        # Обработка команд
        if cmd == 'ls':
            ls(current_path, filesystem)
        elif cmd == 'cd':
            if len(cmd_args) > 0:
                new_path = cd(cmd_args[0], current_path, filesystem)
                if new_path:
                    current_path = new_path
            else:
                print("cd: missing argument")
        elif cmd == 'rev':
            if len(cmd_args) > 0:
                rev(cmd_args[0], filesystem)
            else:
                print("rev: missing argument")
        elif cmd == 'du':
            du(current_path, filesystem)
        elif cmd == 'exit':
            print("Exiting shell emulator...")
            sys.exit(0)
        else:
            print(f"{cmd}: command not found")