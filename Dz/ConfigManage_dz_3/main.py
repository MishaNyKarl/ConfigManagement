
# main.py

import argparse
import yaml
from config_parser import process_input, ConfigParserError

def main():
    parser = argparse.ArgumentParser(description="Парсер учебного конфигурационного языка")
    parser.add_argument("output_file", help="Путь к выходному YAML файлу")
    args = parser.parse_args()

    # Чтение входных данных
    print("Введите текст на учебном конфигурационном языке (Ctrl+D и Enter для завершения):")
    input_text = ""
    try:
        while True:
            line = input()
            if line.strip() == '':
                continue
            input_text += line + "\n"
    except EOFError:
        pass

    # Обработка текста
    try:
        parsed_data = process_input(input_text)
        with open(args.output_file, "w", encoding='utf-8') as yaml_file:
            yaml.dump(parsed_data, yaml_file, default_flow_style=False, allow_unicode=True)
        print(f"Конфигурация успешно сохранена в файл {args.output_file}")
    except ConfigParserError as e:
        print(f"Синтаксическая ошибка: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()

