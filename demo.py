from pathlib import Path

from sipl.parser import parse_ast
from sipl.interpreter.runtime import Interpreter


examples = [
    ("power.sipl", {"X": 2, "Y": 5}),
    ("gcd.sipl", {"M": 8, "N": 16}),
    ("factorial.sipl", {"N": 5})
]


for filename, initial_state in examples:
    source = Path("examples", filename).read_text(
        encoding="utf-8"
    )

    program = parse_ast(source)
    interpreter = Interpreter(initial_state)
    result = interpreter.run(program)

    print(filename)
    print("Initial state:", initial_state)
    print("Final state:", result)
    print()