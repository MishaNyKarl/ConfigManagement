# Парсер учебного конфигурационного языка

---
Это консольное приложение, разработанное для парсинга учебного конфигурационного языка и преобразования его в формат YAML. Программа предоставляет функциональность для анализа конфигурационных файлов, обработки переменных, массивов и словарей, а также визуализации результатов.

---

## Установка

### 1. Клонируйте репозиторий:
```bash
git clone https://github.com/MishaNyKarl/ConfigManagement
```

### 2. Перейдите в директорию с приложением:
```bash
cd ConfigManagement/ConfigParser
```

### 3. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
# Для Windows
venv\Scripts\activate
# Для macOS/Linux
source venv/bin/activate
```

### 4. Установите зависимости из `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Запуск приложения

Запустите основную программу, указав путь к выходному YAML-файлу:
```bash
python main.py output.yaml
```

### Пример:
```bash
python main.py config_output.yaml
```

**Описание ключей командной строки:**

- `output_file`: Путь к выходному YAML-файлу, куда будет сохранен результат парсинга.

## Использование

Программа выполняет следующие шаги:

1. **Чтение входных данных:**
    - Пользователь вводит конфигурационный текст на учебном конфигурационном языке через стандартный ввод.
    - Ввод завершается комбинацией клавиш `Ctrl+Z` и `Enter` (на Windows) или `Ctrl+D` (на macOS/Linux).

2. **Обработка текста:**
    - Парсер анализирует введенный текст, удаляет комментарии и разбивает его на выражения.
    - Обрабатывает объявления переменных, массивы и словари.
    - Проверяет синтаксис и выявляет ошибки.

3. **Сохранение результата:**
    - Преобразованные данные сохраняются в указанный YAML-файл.

![изображение](https://github.com/user-attachments/assets/e91a7aba-53b8-46d3-82b1-632b7b65e50b)
![изображение](https://github.com/user-attachments/assets/f477dbcb-8b7a-4ae0-b2bb-5db0d856b430)



## Пример работы

### Входные данные:
```plaintext
-- Пример конфигурации базы данных
var host := dict(
    name = "db.local",
    port = 5432
);
connections := ({ ![host], ![host], dict(name = "db.remote", port = 5433) });
```

### Команда:
```bash
python main.py config_output.yaml
```

### Результат:
- Создается файл `config_output.yaml` с содержимым:
```yaml
host:
  name: db.local
  port: 5432
connections:
  - name: db.local
    port: 5432
  - name: db.local
    port: 5432
  - name: db.remote
    port: 5433
```

## Запуск тестов

Для обеспечения надежности и корректности парсера предусмотрены модульные тесты. Они проверяют каждую функцию парсера на различных входных данных.

### Запуск тестов:
```bash
python -m unittest test_config_parser.py
```

### Пример запуска:
```bash
python -m unittest test_config_parser.py
```

![изображение](https://github.com/user-attachments/assets/4c9e1d84-a396-46de-8038-16aef0d6da57)



## Поддерживаемые команды

- **Объявление переменных:**
    Используйте `var` для объявления переменных с использованием оператора присваивания `:=`.
    ```plaintext
    var имя := значение;
    ```

- **Присваивание конфигурационных параметров:**
    ```plaintext
    имя := значение;
    ```

- **Словари:**
    ```plaintext
    dict(
        ключ = значение,
        ключ = значение,
        ...
    )
    ```

- **Массивы:**
    ```plaintext
    ({ значение, значение, ... })
    ```

- **Ссылки на переменные:**
    ```plaintext
    ![имя]
    ```

## Примеры использования

### Пример 1: Простое объявление переменной
```plaintext
-- Простая конфигурация
var host := "misha";
```

**Команда:**
```bash
python main.py simple_config.yaml
```

**Результат (`simple_config.yaml`):**
```yaml
host: misha
```

### Пример 2: Конфигурация с словарями и массивами
```plaintext
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
```

**Команда:**
```bash
python main.py app_config.yaml
```

**Результат (`app_config.yaml`):**
```yaml
default_user:
  username: admin
  roles:
    - admin
    - user
users:
  - username: admin
    roles:
      - admin
      - user
  - username: guest
    roles:
      - user
settings:
  debug: 1
  paths:
    - /home
    - /var
```



## Авторы

- **MishaNyKarl** - Идея и реализация
