
# config_parser.py

import re

class ConfigParserError(Exception):
    pass

def process_input(input_text):
    # Удаление однострочных комментариев
    lines = input_text.splitlines()
    code_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith('--') or not line:
            continue
        # Удаляем комментарии после кода
        line = re.split(r'--', line)[0].strip()
        if line:
            code_lines.append(line)
    code = ' '.join(code_lines)

    # Разделение на выражения по ';'
    expressions = [expr.strip() for expr in code.split(';') if expr.strip()]
    
    variables = {}
    config = {}
    for expr in expressions:
        if expr.startswith('var '):
            # Обработка объявления переменной
            match = re.match(r'var\s+([a-zA-Z][a-zA-Z0-9_]*)\s*:=\s*(.+)', expr)
            if not match:
                raise ConfigParserError(f"Неверный синтаксис объявления переменной: '{expr}'")
            var_name, var_value = match.groups()
            if var_name in variables:
                raise ConfigParserError(f"Переменная '{var_name}' уже объявлена")
            variables[var_name] = evaluate_expression(var_value.strip(), variables)
            config[var_name] = variables[var_name]
        else:
            # Обработка присваивания конфигурационных параметров
            match = re.match(r'([a-zA-Z][a-zA-Z0-9_]*)\s*:=\s*(.+)', expr)
            if not match:
                raise ConfigParserError(f"Неверный синтаксис выражения: '{expr}'")
            key, value = match.groups()
            config[key] = evaluate_expression(value.strip(), variables)
    
    return config

def evaluate_expression(expr, variables):
    # Проверка на словарь
    if expr.startswith('dict(') and expr.endswith(')'):
        return parse_dict(expr[5:-1], variables)
    # Проверка на массив
    elif expr.startswith('({') and expr.endswith('})'):
        return parse_array(expr[2:-2], variables)
    # Проверка на переменную
    elif expr.startswith('![') and expr.endswith(']'):
        var_name = expr[2:-1]
        if var_name not in variables:
            raise ConfigParserError(f"Неопределенная переменная: '{var_name}'")
        return variables[var_name]
    # Проверка на число
    elif re.match(r'^-?\d+(\.\d+)?$', expr):
        if '.' in expr:
            return float(expr)
        else:
            return int(expr)
    # Проверка на строку (в кавычках)
    elif (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
        return expr[1:-1]
    else:
        raise ConfigParserError(f"Неверное значение: '{expr}'")

def parse_dict(dict_content, variables):
    result = {}
    # Разделение по запятым, но учитывая возможные вложенные структуры
    tokens = split_tokens(dict_content, ',')
    for token in tokens:
        if '=' not in token:
            raise ConfigParserError(f"Неверный синтаксис словаря: '{token}'")
        key, value = token.split('=', 1)
        key = key.strip()
        value = value.strip()
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', key):
            raise ConfigParserError(f"Неверное имя ключа в словаре: '{key}'")
        result[key] = evaluate_expression(value, variables)
    return result

def parse_array(array_content, variables):
    result = []
    tokens = split_tokens(array_content, ',')
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        result.append(evaluate_expression(token, variables))
    return result

def split_tokens(s, delimiter):
    tokens = []
    current = []
    depth = 0
    i = 0
    while i < len(s):
        c = s[i]
        if c in '({[':
            depth += 1
        elif c in ')}]':
            depth -= 1
        elif c == delimiter and depth == 0:
            tokens.append(''.join(current).strip())
            current = []
            i += 1
            continue
        current.append(c)
        i += 1
    if current:
        tokens.append(''.join(current).strip())
    return tokens
