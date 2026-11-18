import json

from html import escape
from pathlib import Path
from graphviz import Digraph


def to_text(tree, level=0):
    lines = [
        "    " * level + tree["label"]
    ]

    for child in tree["children"]:
        lines.append(to_text(child, level + 1))

    return "\n".join(lines)


def to_json(tree):
    return json.dumps(
        tree,
        indent=2,
        ensure_ascii=False
    )


def to_dot(tree):
    graph = Digraph()
    graph.attr("node", shape="box")

    counter = 0

    def visit(node, parent=None):
        nonlocal counter

        node_id = str(counter)
        counter += 1

        span = node["span"]

        position = (
            f'{span["line"]}:{span["column"]}'
        )

        graph.node(
            node_id,
            node["label"],
            tooltip=position
        )

        if parent is not None:
            graph.edge(parent, node_id)

        for child in node["children"]:
            visit(child, node_id)

    visit(tree)

    return graph.source


def to_html(tree, source):
    span = tree["span"]

    lines = source.splitlines(keepends=True)

    start = (
        sum(len(line) for line in lines[:span["line"] - 1])
        + span["column"] - 1
    )

    end = (
        sum(len(line) for line in lines[:span["end_line"] - 1])
        + span["end_column"] - 1
    )

    fragment = source[start:end]

    label = escape(tree["label"])
    tooltip = escape(fragment, quote=True)

    children = "".join(
        to_html(child, source)
        for child in tree["children"]
    )

    return (
        f'<li><span title="{tooltip}">{label}</span>'
        f'<ul>{children}</ul></li>'
    )


def export_tree(tree, directory, name):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)

    (directory / f"{name}.txt").write_text(
        to_text(tree),
        encoding="utf-8"
    )

    (directory / f"{name}.json").write_text(
        to_json(tree),
        encoding="utf-8"
    )

    (directory / f"{name}.dot").write_text(
        to_dot(tree),
        encoding="utf-8"
    )


def export_comparison(parse_tree, ast_tree, source, directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)

    document = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SIPL Trees</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 30px;
        }}

        .trees {{
            display: flex;
            gap: 40px;
            flex-wrap: wrap;
        }}

        .tree {{
            flex: 1;
            min-width: 300px;
        }}

        ul {{
            padding-left: 25px;
        }}

        li {{
            margin: 8px 0;
        }}

        li span:hover {{
            background: #eeeeee;
        }}

        pre {{
            background: #f5f5f5;
            padding: 15px;
        }}
    </style>
</head>
<body>
    <h1>SIPL Trees</h1>

    <h2>Source code</h2>
    <pre>{escape(source)}</pre>

    <div class="trees">
        <div class="tree">
            <h2>Parse Tree</h2>
            <ul>{to_html(parse_tree, source)}</ul>
        </div>

        <div class="tree">
            <h2>AST</h2>
            <ul>{to_html(ast_tree, source)}</ul>
        </div>
    </div>
</body>
</html>
"""

    path = directory / "comparison.html"

    path.write_text(
        document,
        encoding="utf-8"
    )

    return path