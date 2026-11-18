# Conformance Suite

Набір тестів tests/conformance/cases.json призначений
для перевірки відповідності реалізації специфікації SIPL.

## Формат тестів

- name — назва тесту.
- source — текст SIPL-програми.
- initial_state — початковий стан змінних.
- expected_state — очікуваний кінцевий стан.
- expected_ast — очікувана структура AST.
- expected_error — тип очікуваної помилки.
- max_steps — максимальна кількість кроків.

Поле expected_ast може містити часткову структуру
дерева. Перевіряються лише зазначені поля.

## Запуск

    $env:PYTHONPATH = "src"
    $env:PYTHONIOENCODING = "utf-8"

    .\venv\Scripts\python.exe tests\conformance\runner.py --command .\venv\Scripts\python.exe -m sipl.cli

Засіб перевірки не залежить від внутрішньої реалізації
SIPL та використовує консольний інтерфейс.

Коди завершення:

0 — усі тести пройдено.
1 — принаймні один тест не пройдено.