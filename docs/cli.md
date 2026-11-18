# Консольний інтерфейс SIPL

## Команди

- parse — побудова AST.
- check — перевірка синтаксису.
- run — виконання програми.
- trace — покрокове виконання.
- visualize — візуалізація синтаксичного дерева та AST.

## Параметри

- --state — початковий стан у форматі JSON.
- --max-steps — максимальна кількість кроків.
- --json — структурований результат.
- --output — папка для збереження результатів візуалізації.

## Коди завершення

0 — успішне виконання.
1 — синтаксична помилка.
2 — помилка виконання.
3 — помилка вхідних даних.

Помилки аргументів argparse мають код 2.

## Формат JSON

Успішний результат містить status: ok.

Команда parse додатково повертає ast.
Команда check повертає message.
Команда run повертає state та steps.
Команда trace повертає state, steps та trace.
Команда visualize повертає message та file.

Помилка містить status: error, type та message.
Синтаксична помилка також містить line та column.

## Події trace

- ProgramStarted
- BeforeStatement
- VariableChanged
- ConditionChecked
- AfterStatement
- ProgramFinished
- ProgramFailed

Кожна подія містить номер кроку та копію стану.
Події, пов'язані з AST, містять тип вузла та SourceSpan.
