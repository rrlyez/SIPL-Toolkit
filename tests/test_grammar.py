import pytest
from lark.exceptions import UnexpectedInput
from sipl.parser import parse


@pytest.mark.parametrize("source", [
    "begin skip end",
    "begin X := 5 end",
    "begin X := -5 end",
    "begin X := 2 + 3 * 4 end",
    "begin X := (2 + 3) * 4 end",
    "begin X := 10 - 3 - 2 end",
    "begin X := 1; Y := X + 2 end",
    "begin if X > 0 then X := 1 else X := 0 end",
    "begin while X > 0 do X := X - 1 end",
    "begin begin X := 1; Y := 2 end end",
    "begin if ¬(X = 0) then skip else X := 1 end",
    "begin if X = 0 ∨ Y > 1 then skip else skip end",
])
def test_valid_program(source):
    assert parse(source) is not None


@pytest.mark.parametrize("source", [
    "",
    "X := 5",
    "begin end",
    "begin X := end",
    "begin X = 5 end",
    "begin X := 1; end",
    "begin X := 1 Y := 2 end",
    "begin if X > 0 then skip end",
    "begin while X > 0 skip end",
    "begin X := (2 + 3 end",
    "begin X := 10 / 2 end",
    "begin skip",
])
def test_invalid_program(source):
    with pytest.raises(UnexpectedInput):
        parse(source)