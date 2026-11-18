import pytest

from sipl.parser import parse_ast
from sipl.interpreter.runtime import (
    Interpreter,
    SIPLRuntimeError
)


def run(source, state=None, max_steps=10000):
    program = parse_ast(source)
    interpreter = Interpreter(state, max_steps)
    return interpreter.run(program)


def test_assignment():
    assert run("begin X := 5 end") == {"X": 5}


def test_addition():
    assert run("begin X := 2 + 3 end") == {"X": 5}


def test_subtraction():
    assert run("begin X := 10 - 3 end") == {"X": 7}


def test_multiplication():
    assert run("begin X := 4 * 3 end") == {"X": 12}


def test_priority():
    assert run("begin X := 2 + 3 * 4 end") == {"X": 14}


def test_parentheses():
    assert run("begin X := (2 + 3) * 4 end") == {"X": 20}


def test_negative_number():
    assert run("begin X := -5 end") == {"X": -5}


def test_sequence():
    assert run(
        "begin X := 5; Y := X + 2 end"
    ) == {"X": 5, "Y": 7}


def test_if_true():
    source = """
    begin
        if X > 0 then Y := 1 else Y := 0
    end
    """
    assert run(source, {"X": 5}) == {"X": 5, "Y": 1}


def test_if_false():
    source = """
    begin
        if X > 0 then Y := 1 else Y := 0
    end
    """
    assert run(source, {"X": -5}) == {"X": -5, "Y": 0}


def test_equality():
    source = "begin if X = 5 then Y := 1 else Y := 0 end"
    assert run(source, {"X": 5})["Y"] == 1


def test_negation():
    source = "begin if ¬(X = 0) then Y := 1 else Y := 0 end"
    assert run(source, {"X": 5})["Y"] == 1


def test_disjunction():
    source = """
    begin
        if X = 0 ∨ X > 5 then Y := 1 else Y := 0
    end
    """
    assert run(source, {"X": 10})["Y"] == 1


def test_while():
    source = """
    begin
        while X > 0 do X := X - 1
    end
    """
    assert run(source, {"X": 5}) == {"X": 0}


def test_block():
    assert run(
        "begin begin X := 5; Y := 2 end end"
    ) == {"X": 5, "Y": 2}


def test_skip():
    assert run("begin skip end", {"X": 5}) == {"X": 5}


def test_undefined_variable():
    with pytest.raises(SIPLRuntimeError):
        run("begin X := Y end")


def test_infinite_loop():
    with pytest.raises(SIPLRuntimeError):
        run(
            "begin while 1 = 1 do skip end",
            max_steps=100
        )


def test_initial_state():
    state = {"X": 5}

    result = run("begin X := X + 1 end", state)

    assert result == {"X": 6}
    assert state == {"X": 5}