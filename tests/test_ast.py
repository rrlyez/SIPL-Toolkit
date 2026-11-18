import pytest

from sipl.parser import parse_ast, SIPLSyntaxError
from sipl.ast import (
    Program,
    Assign,
    Number,
    Variable,
    BinaryOp,
    Sequence,
    If,
    While,
    Block,
    Skip
)


def test_program():
    ast = parse_ast("begin skip end")

    assert isinstance(ast, Program)
    assert isinstance(ast.body, Skip)


def test_assignment():
    ast = parse_ast("begin X := 5 end")

    assert isinstance(ast.body, Assign)
    assert ast.body.name == "X"
    assert isinstance(ast.body.value, Number)
    assert ast.body.value.value == 5


def test_variable():
    ast = parse_ast("begin X := Y end")

    assert isinstance(ast.body.value, Variable)
    assert ast.body.value.name == "Y"


def test_priority():
    ast = parse_ast("begin X := 2 + 3 * 4 end")
    expr = ast.body.value

    assert isinstance(expr, BinaryOp)
    assert expr.operator == "+"
    assert expr.right.operator == "*"


def test_sequence():
    ast = parse_ast("begin X := 1; Y := 2 end")

    assert isinstance(ast.body, Sequence)
    assert ast.body.first.name == "X"
    assert ast.body.second.name == "Y"


def test_if():
    ast = parse_ast(
        "begin if X > 0 then skip else skip end"
    )

    assert isinstance(ast.body, If)
    assert ast.body.condition.operator == ">"


def test_while():
    ast = parse_ast(
        "begin while X > 0 do X := X - 1 end"
    )

    assert isinstance(ast.body, While)
    assert isinstance(ast.body.body, Assign)


def test_block():
    ast = parse_ast("begin begin skip end end")

    assert isinstance(ast.body, Block)
    assert isinstance(ast.body.body, Skip)


def test_source_span():
    ast = parse_ast("begin\n    X := 5\nend")

    assert ast.body.span.line == 2
    assert ast.body.span.column == 5


def test_syntax_error():
    with pytest.raises(SIPLSyntaxError) as error:
        parse_ast("begin\n    X :=\nend")

    assert error.value.line == 3
    assert error.value.column == 1
    assert "Syntax error" in str(error.value)