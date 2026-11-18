import json

from sipl.parser import parse, parse_ast

from sipl.visualization.trees import (
    parse_tree_data,
    ast_tree_data
)

from sipl.visualization.export import (
    to_text,
    to_json,
    to_dot,
    export_tree,
    export_comparison
)

from sipl.cli import main


SOURCE = "begin X := 2 + 3 end"


def test_parse_tree():
    tree = parse_tree_data(parse(SOURCE))

    assert tree["label"] == "start"
    assert tree["children"]


def test_ast_tree():
    tree = ast_tree_data(parse_ast(SOURCE))

    assert tree["label"] == "Program"
    assert tree["children"][0]["label"] == "Assign: X"


def test_text_export():
    tree = ast_tree_data(parse_ast(SOURCE))
    result = to_text(tree)

    assert "Program" in result
    assert "Assign: X" in result
    assert "BinaryOp: +" in result


def test_json_export():
    tree = ast_tree_data(parse_ast(SOURCE))
    result = json.loads(to_json(tree))

    assert result == tree


def test_dot_export():
    tree = ast_tree_data(parse_ast(SOURCE))
    result = to_dot(tree)

    assert "digraph" in result
    assert "Program" in result
    assert "Assign: X" in result


def test_tree_span():
    tree = parse_tree_data(
        parse("begin\n    X := 5\nend")
    )

    program = tree["children"][0]
    assignment = program["children"][1]

    assert assignment["span"]["line"] == 2
    assert assignment["span"]["column"] == 5


def test_export_files(tmp_path):
    tree = ast_tree_data(parse_ast(SOURCE))

    export_tree(tree, tmp_path, "ast")

    assert (tmp_path / "ast.txt").exists()
    assert (tmp_path / "ast.json").exists()
    assert (tmp_path / "ast.dot").exists()


def test_html_comparison(tmp_path):
    concrete = parse_tree_data(parse(SOURCE))
    abstract = ast_tree_data(parse_ast(SOURCE))

    file = export_comparison(
        concrete,
        abstract,
        SOURCE,
        tmp_path
    )

    content = file.read_text(encoding="utf-8")

    assert "Parse Tree" in content
    assert "AST" in content
    assert SOURCE in content
    assert "title=" in content


def test_visualize_cli(tmp_path):
    file = tmp_path / "program.sipl"
    file.write_text(SOURCE, encoding="utf-8")

    directory = tmp_path / "output"

    code = main([
        "visualize",
        str(file),
        "--output",
        str(directory)
    ])

    assert code == 0
    assert (directory / "comparison.html").exists()
    assert (directory / "parse_tree.dot").exists()
    assert (directory / "ast.dot").exists()