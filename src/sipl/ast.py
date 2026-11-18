from dataclasses import dataclass


@dataclass
class SourceSpan:
    line: int
    column: int
    end_line: int
    end_column: int


@dataclass
class Node:
    span: SourceSpan


@dataclass
class Expression(Node):
    pass


@dataclass
class Statement(Node):
    pass


@dataclass
class Number(Expression):
    value: int


@dataclass
class Variable(Expression):
    name: str


@dataclass
class BinaryOp(Expression):
    operator: str
    left: Expression
    right: Expression


@dataclass
class UnaryOp(Expression):
    operator: str
    operand: Expression


@dataclass
class Assign(Statement):
    name: str
    value: Expression


@dataclass
class Sequence(Statement):
    first: Statement
    second: Statement


@dataclass
class If(Statement):
    condition: Expression
    then_branch: Statement
    else_branch: Statement


@dataclass
class While(Statement):
    condition: Expression
    body: Statement


@dataclass
class Block(Statement):
    body: Statement


@dataclass
class Skip(Statement):
    pass


@dataclass
class Program(Node):
    body: Statement