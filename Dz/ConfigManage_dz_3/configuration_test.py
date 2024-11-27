# configuration_test.py

test_input_0 = """
-- Hello
var host = "misha"
"""


test_input_1 = """
-- Пример конфигурации базы данных
var host := dict(
    name = "db.local",
    port = 5432
);
connections = ({ ![host], ![host], dict(name = "db.remote", port = 5433) });
"""

test_input_2 = """
-- Пример конфигурации приложения
var default_user := dict(
    username = "admin",
    roles = ({ "admin", "user" })
);
users = ({ ![default_user], dict(username = "guest", roles = ({ "user" })) });
settings = dict(
    debug = 1,
    paths = ({ "/home", "/var" })
);
"""

def run_test(input_text):
    from config_parser import process_input
    import yaml
    parsed_data = process_input(input_text)
    print(yaml.dump(parsed_data, default_flow_style=False, allow_unicode=True))

if __name__ == "__main__":
    print('Тест 0:')
    run_test(test_input_0)
    print("Тест 1:")
    run_test(test_input_1)
    print("\nТест 2:")
    run_test(test_input_2)
