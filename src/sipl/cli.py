import argparse
import json
import re
import sys

from pathlib import Path

from sipl.parser import parse, parse_ast, SIPLSyntaxError

from sipl.visualization.trees import (
    parse_tree_data,
    ast_tree_data
)

from sipl.visualization.export import (
    export_tree,
    export_comparison
)

from sipl.serialization import to_data
from sipl.interpreter.runtime import (
    Interpreter,
    SIPLRuntimeError
)


def output(data):
    print(json.dumps(
        data,
        indent=2,
        ensure_ascii=False
    ))


def read_state(text):
    state = json.loads(text)

    if not isinstance(state, dict):
        raise ValueError("State must be a JSON object")

    keywords = {
        "begin", "end", "if", "then",
        "else", "while", "do", "skip"
    }

    for name, value in state.items():
        if (
            not re.fullmatch(
                r"[a-zA-Z][a-zA-Z0-9_]*", name
            )
            or name in keywords
        ):
            raise ValueError(f"Invalid variable: {name}")

        if type(value) is not int:
            raise ValueError(
                "State values must be integers"
            )

    return state


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="SIPL Language Toolkit"
    )

    parser.add_argument(
        "command",
        choices=["parse", "check", "run", "trace", "visualize"]
    )

    parser.add_argument("file")

    parser.add_argument(
        "--output",
        default="output"
    )

    parser.add_argument(
        "--state",
        default="{}",
        help="Initial state as JSON"
    )

    parser.add_argument(
        "--max-steps",
        type=int,
        default=10000
    )

    parser.add_argument(
        "--json",
        action="store_true"
    )

    args = parser.parse_args(argv)

    interpreter = None

    try:
        source = Path(args.file).read_text(
            encoding="utf-8"
        )

        program = parse_ast(source)

        if args.command == "parse":
            result = {
                "status": "ok",
                "ast": to_data(program)
            }

        elif args.command == "check":
            result = {
                "status": "ok",
                "message": "Syntax is valid"
            }

        elif args.command == "visualize":
            concrete = parse_tree_data(parse(source))
            abstract = ast_tree_data(program)

            export_tree(
                concrete,
                args.output,
                "parse_tree"
            )

            export_tree(
                abstract,
                args.output,
                "ast"
            )

            path = export_comparison(
                concrete,
                abstract,
                source,
                args.output
            )

            result = {
                "status": "ok",
                "message": "Trees exported successfully",
                "file": str(path)
            }

        else:
            state = read_state(args.state)

            if args.max_steps <= 0:
                raise ValueError(
                    "Step limit must be positive"
                )

            interpreter = Interpreter(
                state,
                args.max_steps
            )

            final_state = interpreter.run(program)

            result = {
                "status": "ok",
                "state": final_state,
                "steps": interpreter.steps
            }

            if args.command == "trace":
                result["trace"] = interpreter.trace

        if args.json:
            output(result)

        elif args.command == "check":
            print(result["message"])

        elif args.command == "visualize":
            print(result["message"])
            print("File:", result["file"])
        
        elif args.command == "parse":
            output(result["ast"])

        elif args.command == "run":
            print("Final state:", result["state"])
            print("Steps:", result["steps"])

        elif args.command == "trace":
            for event in result["trace"]:
                print(
                    event["step"],
                    event["event"],
                    event["state"]
                )

            print("Final state:", result["state"])

        return 0

    except SIPLSyntaxError as error:
        result = {
            "status": "error",
            "type": "syntax",
            "message": str(error),
            "line": error.line,
            "column": error.column
        }

        code = 1

    except SIPLRuntimeError as error:
        result = {
            "status": "error",
            "type": "runtime",
            "message": str(error)
        }

        if args.command == "trace":
            result["trace"] = interpreter.trace

        code = 2

    except (OSError, ValueError) as error:
        result = {
            "status": "error",
            "type": "input",
            "message": str(error)
        }

        code = 3

    if args.json:
        output(result)
    else:
        print(
            result["message"],
            file=sys.stderr
        )

    return code


if __name__ == "__main__":
    sys.exit(main())