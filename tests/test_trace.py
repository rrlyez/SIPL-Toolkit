import pytest

from sipl.parser import parse_ast
from sipl.interpreter.runtime import (
    Interpreter,
    SIPLRuntimeError
)


def test_trace_events():
    interpreter = Interpreter()
    interpreter.run(parse_ast("begin X := 5 end"))

    events = [
        item["event"] for item in interpreter.trace
    ]

    assert events == [
        "ProgramStarted",
        "BeforeStatement",
        "VariableChanged",
        "AfterStatement",
        "ProgramFinished"
    ]


def test_variable_changed():
    interpreter = Interpreter({"X": 2})
    interpreter.run(parse_ast("begin X := X + 3 end"))

    changes = [
        item for item in interpreter.trace
        if item["event"] == "VariableChanged"
    ]

    assert changes[0]["variable"] == "X"
    assert changes[0]["old_value"] == 2
    assert changes[0]["new_value"] == 5


def test_condition_checked():
    interpreter = Interpreter({"X": 2})

    interpreter.run(parse_ast(
        "begin while X > 0 do X := X - 1 end"
    ))

    results = [
        item["result"] for item in interpreter.trace
        if item["event"] == "ConditionChecked"
    ]

    assert results == [True, True, False]


def test_state_snapshot():
    interpreter = Interpreter()

    interpreter.run(parse_ast(
        "begin X := 1; X := 2 end"
    ))

    changes = [
        item for item in interpreter.trace
        if item["event"] == "VariableChanged"
    ]

    assert changes[0]["state"] == {"X": 1}
    assert changes[1]["state"] == {"X": 2}


def test_trace_error():
    interpreter = Interpreter()

    with pytest.raises(SIPLRuntimeError):
        interpreter.run(parse_ast("begin X := Y end"))

    assert interpreter.trace[-1]["event"] == "ProgramFailed"


def test_trace_span():
    interpreter = Interpreter()

    interpreter.run(parse_ast(
        "begin\n    X := 5\nend"
    ))

    change = next(
        item for item in interpreter.trace
        if item["event"] == "VariableChanged"
    )

    assert change["span"]["line"] == 2
    assert change["span"]["column"] == 5