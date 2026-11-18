import argparse
import json
import subprocess
import tempfile
import sys

from pathlib import Path


def matches(actual, expected):
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(
            key in actual and matches(actual[key], value)
            for key, value in expected.items()
        )

    if isinstance(expected, list):
        return (
            isinstance(actual, list)
            and len(actual) == len(expected)
            and all(
                matches(a, b)
                for a, b in zip(actual, expected)
            )
        )

    return actual == expected


def execute(command, arguments):
    process = subprocess.run(
        command + arguments,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30
    )

    return process.returncode, json.loads(process.stdout)


def check_case(case, command, file):
    if "expected_ast" in case:
        code, parsed = execute(command, [
            "parse",
            str(file),
            "--json"
        ])

        assert code == 0
        assert matches(
            parsed["ast"],
            case["expected_ast"]
        )

    code, result = execute(command, [
        "run",
        str(file),
        "--state",
        json.dumps(case["initial_state"]),
        "--max-steps",
        str(case.get("max_steps", 10000)),
        "--json"
    ])

    if "expected_error" in case:
        assert code != 0
        assert result["status"] == "error"
        assert result["type"] == case["expected_error"]

    else:
        assert code == 0
        assert result["status"] == "ok"
        assert result["state"] == case["expected_state"]


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--command",
        nargs=argparse.REMAINDER,
        required=True
    )

    args = parser.parse_args()

    cases_path = Path(__file__).with_name("cases.json")

    cases = json.loads(
        cases_path.read_text(encoding="utf-8")
    )

    passed = 0

    with tempfile.TemporaryDirectory() as directory:
        file = Path(directory) / "program.sipl"

        for case in cases:
            file.write_text(
                case["source"],
                encoding="utf-8"
            )

            try:
                check_case(case, args.command, file)
                print("PASS:", case["name"])
                passed += 1

            except Exception as error:
                print("FAIL:", case["name"], repr(error))

    print(f"\nPassed: {passed}/{len(cases)}")

    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())