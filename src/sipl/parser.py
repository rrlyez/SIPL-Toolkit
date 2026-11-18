from pathlib import Path
from lark import Lark, Tree
from lark.exceptions import UnexpectedInput

from .ast import (
    SourceSpan,
    Program,
    Number,
    Variable,
    BinaryOp,
    UnaryOp,
    Assign,
    Sequence,
    If,
    While,
    Block,
    Skip
)


grammar_path = (
    Path(__file__).resolve().parents[2]
    / "grammar"
    / "sipl.lark"
)

parser = Lark(
    grammar_path.read_text(encoding="utf-8"),
    parser="lalr",
    propagate_positions=True,
    keep_all_tokens=True
)


def parse(source):
    return parser.parse(source)


def get_span(tree):
    return SourceSpan(
        line=tree.meta.line,
        column=tree.meta.column,
        end_line=tree.meta.end_line,
        end_column=tree.meta.end_column
    )


def build_ast(tree):
    kind = tree.data
    children = tree.children
    span = get_span(tree)

    if kind == "start":
        return build_ast(children[0])

    if kind == "program":
        return Program(span, build_ast(children[1]))

    if kind == "number":
        return Number(span, int(children[0]))

    if kind == "variable":
        return Variable(span, str(children[0]))

    operators = {
        "add": "+",
        "sub": "-",
        "mult": "*",
        "eq": "=",
        "gr": ">",
        "or_expr": "∨"
    }

    if kind in operators:
        return BinaryOp(
            span,
            operators[kind],
            build_ast(children[0]),
            build_ast(children[2])
        )

    if kind == "not_expr":
        return UnaryOp(
            span,
            "¬",
            build_ast(children[1])
        )

    if kind in ("arith_group", "bool_group"):
        node = build_ast(children[1])
        node.span = span
        return node

    if kind == "assign":
        return Assign(
            span,
            str(children[0]),
            build_ast(children[2])
        )

    if kind == "sequence":
        return Sequence(
            span,
            build_ast(children[0]),
            build_ast(children[2])
        )

    if kind == "if_stmt":
        return If(
            span,
            build_ast(children[1]),
            build_ast(children[3]),
            build_ast(children[5])
        )

    if kind == "while_stmt":
        return While(
            span,
            build_ast(children[1]),
            build_ast(children[3])
        )

    if kind == "block":
        return Block(span, build_ast(children[1]))

    if kind == "skip":
        return Skip(span)

    raise ValueError(f"Unknown node: {kind}")


class SIPLSyntaxError(Exception):
    def __init__(self, message, line, column):
        super().__init__(message)
        self.line = line
        self.column = column


def parse_ast(source):
    try:
        return build_ast(parse(source))
    except UnexpectedInput as error:
        message = (
            f"Syntax error at line {error.line}, "
            f"column {error.column}\n"
            f"{error.get_context(source)}"
        )

        raise SIPLSyntaxError(
            message,
            error.line,
            error.column
        ) from error


if __name__ == "__main__":
    from dataclasses import asdict
    import json

    source = """
begin
    X := 5;
    Y := 2;
    Z := X * Y
end
"""

    try:
        ast = parse_ast(source)

        print(json.dumps(
            asdict(ast),
            indent=4,
            ensure_ascii=False
        ))

    except SIPLSyntaxError as error:
        print(error)