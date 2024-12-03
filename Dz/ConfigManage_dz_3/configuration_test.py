
# configuration_test.py

import yaml
from config_parser import process_input, ConfigParserError

test_input_0 = """
-- Hello
var host := "misha";
"""

test_input_1 = """
-- Пример конфигурации базы данных
var host := dict(
    name = "db.local",
    port = 5432
);
connections := ({ ![host], ![host], dict(name = "db.remote", port = 5433) });
"""

test_input_2 = """
-- Пример конфигурации приложения
var default_user := dict(
    username = "admin",
    roles = ({ "admin", "user" })
);
users := ({ ![default_user], dict(username = "guest", roles = ({ "user" })) });
settings := dict(
    debug = 1,
    paths = ({ "/home", "/var" })
);
"""

def run_test(input_text, test_number):
    print(f'Тест {test_number}:')
    try:
        parsed_data = process_input(input_text)
        # Для улучшения читаемости уберем YAML-якоря
        print(yaml.dump(parsed_data, default_flow_style=False, allow_unicode=True, sort_keys=False))
    except ConfigParserError as e:
        print(f"Синтаксическая ошибка: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")
    print("-" * 40)

if __name__ == "__main__":
    run_test(test_input_0, 0)
    run_test(test_input_1, 1)
    run_test(test_input_2, 2)

