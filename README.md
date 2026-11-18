# SIPL Language Toolkit

Набір інструментів для аналізу, виконання та
візуалізації програм мовою SIPL.

Проєкт з дисципліни «Теорія програмування».

## Реалізовані модулі

| ID | Завдання | Бали |
|---|---|---:|
| CORE-01 | Формальна граматика SIPL | 0.5 |
| CORE-02 | Парсер та AST | 1.5 |
| CORE-03 | Інтерпретатор | 2.0 |
| CORE-04 | Покрокове виконання | 1.0 |
| CORE-05 | Консольний інтерфейс | 1.0 |
| CORE-06 | Conformance suite | 1.0 |
| VIS-01 | Синтаксичне дерево | 1.5 |
| VIS-02 | Візуалізація AST | 1.0 |
| REL-02 | GitHub Release | 0.5 |

Заявлена сума: 10 балів.

## Встановлення

Python 3.14.

Команди для Windows PowerShell:

    py -m venv venv

    .\venv\Scripts\python.exe -m pip install -r requirements.txt

    $env:PYTHONPATH = "src"

    $env:PYTHONIOENCODING = "utf-8"

## Запуск прикладів

    .\venv\Scripts\python.exe demo.py

## Перевірка синтаксису

    .\venv\Scripts\python.exe -m sipl.cli check examples\power.sipl

## Побудова AST

    .\venv\Scripts\python.exe -m sipl.cli parse examples\power.sipl

## Виконання програми

    .\venv\Scripts\python.exe -m sipl.cli run examples\power.sipl --state '{\"X\":2,\"Y\":5}'

## Покрокове виконання

    .\venv\Scripts\python.exe -m sipl.cli trace examples\power.sipl --state '{\"X\":2,\"Y\":5}'

Для отримання структурованого результату
використовується параметр --json.

## Візуалізація

    .\venv\Scripts\python.exe -m sipl.cli visualize examples\power.sipl

    start output\comparison.html

Підтримуються формати TXT, JSON, DOT та HTML.

## Тестування

    .\venv\Scripts\python.exe -m pytest

Перевірка покриття:

    .\venv\Scripts\python.exe -m pytest --cov=sipl --cov-report=term-missing

Conformance suite:

    .\venv\Scripts\python.exe tests\conformance\runner.py --command .\venv\Scripts\python.exe -m sipl.cli

## Обмеження

Підтримується базова мова SIPL без рекурсивних функцій.

Виконання обмежується максимальною кількістю кроків.

Звернення до невизначеної змінної викликає помилку.

Синтаксис і пріоритети операцій відповідають
матеріалам курсу. Уточнення лексики наведені
в документації.

## Документація

- [Граматика](docs/grammar.md)
- [Консольний інтерфейс](docs/cli.md)
- [Conformance suite](docs/conformance.md)
- [Візуалізація](docs/visualization.md)

