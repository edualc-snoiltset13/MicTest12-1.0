import math
import pytest

from calculator import CalculatorError, EvalError, ParseError, evaluate


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("1 + 2", 3),
        ("2 - 5", -3),
        ("3 * 4", 12),
        ("10 / 4", 2.5),
        ("10 // 3", 3),
        ("10 % 3", 1),
        ("2 ** 10", 1024),
        ("-3 + 4", 1),
        ("--3", 3),
        ("(1 + 2) * 3", 9),
        ("1 + 2 * 3", 7),
        ("2 ** 3 ** 2", 512),  # right-associative
        ("1.5 + 2.5", 4.0),
        ("1e3 + 1", 1001.0),
        ("((1)) + ((2 * 3))", 7),
    ],
)
def test_evaluate_ok(expr, expected):
    result = evaluate(expr)
    if isinstance(expected, float):
        assert math.isclose(result, expected)
    else:
        assert result == expected


@pytest.mark.parametrize(
    "expr, exc",
    [
        ("", ParseError),
        ("1 +", ParseError),
        ("(1 + 2", ParseError),
        ("1 + )", ParseError),
        ("1 / 0", EvalError),
        ("1 // 0", EvalError),
        ("1 % 0", EvalError),
        ("1 + abc", Exception),  # tokenizer raises LexError -> CalculatorError subclass
    ],
)
def test_evaluate_errors(expr, exc):
    with pytest.raises(CalculatorError if exc is Exception else exc):
        evaluate(expr)
