from dataclasses import fields, asdict
from lark import Tree, Token

from sipl.ast import Node


def parse_tree_data(node):
    if isinstance(node, Token):
        return {
            "label": str(node),
            "type": node.type,
            "span": {
                "line": node.line,
                "column": node.column,
                "end_line": node.end_line,
                "end_column": node.end_column
            },
            "children": []
        }

    if isinstance(node, Tree):
        return {
            "label": str(node.data),
            "type": "rule",
            "span": {
                "line": node.meta.line,
                "column": node.meta.column,
                "end_line": node.meta.end_line,
                "end_column": node.meta.end_column
            },
            "children": [
                parse_tree_data(child)
                for child in node.children
            ]
        }

    raise TypeError("Unknown tree node")


def ast_tree_data(node):
    label = type(node).__name__
    children = []

    for field in fields(node):
        if field.name == "span":
            continue

        value = getattr(node, field.name)

        if isinstance(value, Node):
            children.append(ast_tree_data(value))
        else:
            label += f": {value}"

    return {
        "label": label,
        "type": type(node).__name__,
        "span": asdict(node.span),
        "children": children
    }