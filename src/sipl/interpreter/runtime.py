from dataclasses import asdict

from sipl.ast import (
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


class SIPLRuntimeError(Exception):
    pass


class Interpreter:
    def __init__(self, initial_state=None, max_steps=10000):
        self.initial_state = dict(initial_state or {})
        self.state = self.initial_state.copy()
        self.max_steps = max_steps
        self.steps = 0
        self.trace = []

    def tick(self):
        self.steps += 1

        if self.steps > self.max_steps:
            raise SIPLRuntimeError(
                "Execution step limit exceeded"
            )

    def emit(self, event, node=None, **details):
        record = {
            "event": event,
            "step": self.steps,
            "state": self.state.copy()
        }

        if node is not None:
            record["node"] = type(node).__name__
            record["span"] = asdict(node.span)

        record.update(details)
        self.trace.append(record)

    def evaluate(self, node):
        if isinstance(node, Number):
            return node.value

        if isinstance(node, Variable):
            if node.name not in self.state:
                raise SIPLRuntimeError(
                    f"Undefined variable: {node.name}"
                )

            return self.state[node.name]

        if isinstance(node, UnaryOp):
            if node.operator == "¬":
                return not self.evaluate(node.operand)

        if isinstance(node, BinaryOp):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            if node.operator == "+":
                return left + right

            if node.operator == "-":
                return left - right

            if node.operator == "*":
                return left * right

            if node.operator == "=":
                return left == right

            if node.operator == ">":
                return left > right

            if node.operator == "∨":
                return left or right

        raise SIPLRuntimeError("Unknown expression")

    def check_condition(self, node):
        result = self.evaluate(node)

        self.emit(
            "ConditionChecked",
            node,
            result=result
        )

        return result

    def execute(self, node):
        self.tick()
        self.emit("BeforeStatement", node)

        if isinstance(node, Assign):
            old_value = self.state.get(node.name)
            new_value = self.evaluate(node.value)

            self.state[node.name] = new_value

            self.emit(
                "VariableChanged",
                node,
                variable=node.name,
                old_value=old_value,
                new_value=new_value
            )

        elif isinstance(node, Sequence):
            self.execute(node.first)
            self.execute(node.second)

        elif isinstance(node, If):
            if self.check_condition(node.condition):
                self.execute(node.then_branch)
            else:
                self.execute(node.else_branch)

        elif isinstance(node, While):
            while True:
                self.tick()

                if not self.check_condition(node.condition):
                    break

                self.execute(node.body)

        elif isinstance(node, Block):
            self.execute(node.body)

        elif isinstance(node, Skip):
            pass

        else:
            raise SIPLRuntimeError("Unknown statement")

        self.emit("AfterStatement", node)

    def run(self, program):
        self.steps = 0
        self.trace = []
        self.state = self.initial_state.copy()

        self.emit("ProgramStarted", program)

        try:
            self.execute(program.body)

        except SIPLRuntimeError as error:
            self.emit(
                "ProgramFailed",
                program,
                message=str(error)
            )
            raise

        self.emit("ProgramFinished", program)

        return self.state.copy()