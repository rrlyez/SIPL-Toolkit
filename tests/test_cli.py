import json

from sipl.cli import main


def create_program(tmp_path, source):
    file = tmp_path / "test.sipl"
    file.write_text(source, encoding="utf-8")
    return str(file)


def test_check(tmp_path, capsys):
    file = create_program(tmp_path, "begin skip end")

    assert main(["check", file]) == 0
    assert "Syntax is valid" in capsys.readouterr().out


def test_parse(tmp_path, capsys):
    file = create_program(tmp_path, "begin X := 5 end")

    assert main(["parse", file, "--json"]) == 0

    result = json.loads(capsys.readouterr().out)

    assert result["ast"]["type"] == "Program"
    assert result["ast"]["body"]["type"] == "Assign"


def test_run(tmp_path, capsys):
    file = create_program(tmp_path, "begin X := X + 2 end")

    assert main([
        "run", file,
        "--state", '{"X": 5}',
        "--json"
    ]) == 0

    result = json.loads(capsys.readouterr().out)
    assert result["state"] == {"X": 7}


def test_trace(tmp_path, capsys):
    file = create_program(tmp_path, "begin X := 5 end")

    assert main(["trace", file, "--json"]) == 0

    result = json.loads(capsys.readouterr().out)

    assert result["trace"][-1]["event"] == "ProgramFinished"


def test_syntax_error(tmp_path, capsys):
    file = create_program(tmp_path, "begin X := end")

    assert main(["check", file, "--json"]) == 1

    result = json.loads(capsys.readouterr().out)

    assert result["type"] == "syntax"
    assert "line" in result
    assert "column" in result


def test_runtime_error(tmp_path, capsys):
    file = create_program(tmp_path, "begin X := Y end")

    assert main(["run", file, "--json"]) == 2

    result = json.loads(capsys.readouterr().out)
    assert result["type"] == "runtime"


def test_invalid_state(tmp_path, capsys):
    file = create_program(tmp_path, "begin skip end")

    assert main([
        "run", file,
        "--state", '{"X": "abc"}',
        "--json"
    ]) == 3

    result = json.loads(capsys.readouterr().out)
    assert result["type"] == "input"


def test_missing_file(tmp_path):
    file = str(tmp_path / "missing.sipl")

    assert main(["run", file]) == 3