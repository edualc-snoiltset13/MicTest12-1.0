"""Safe arithmetic expression calculator.

Supports + - * / // % ** with parentheses and unary +/-.
Numbers may be ints or floats (including scientific notation, e.g. 1.2e-3).
Evaluation is implemented with a hand-written recursive-descent parser, so
no `eval`/`exec` is used and only arithmetic on numeric literals is possible.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Union

Number = Union[int, float]


class CalculatorError(Exception):
    """Base class for calculator errors."""


class LexError(CalculatorError):
    pass


class ParseError(CalculatorError):
    pass


class EvalError(CalculatorError):
    pass


@dataclass(frozen=True)
class Token:
    kind: str   # 'NUM', 'OP', 'LP', 'RP'
    value: str
    pos: int


_OPS = {"+", "-", "*", "/", "//", "%", "**"}


def tokenize(src: str) -> list[Token]:
    tokens: list[Token] = []
    i = 0
    n = len(src)
    while i < n:
        c = src[i]
        if c.isspace():
            i += 1
            continue
        if c == "(":
            tokens.append(Token("LP", c, i))
            i += 1
            continue
        if c == ")":
            tokens.append(Token("RP", c, i))
            i += 1
            continue
        if c in "+-*/%":
            two = src[i : i + 2]
            if two in {"**", "//"}:
                tokens.append(Token("OP", two, i))
                i += 2
            else:
                tokens.append(Token("OP", c, i))
                i += 1
            continue
        if c.isdigit() or c == ".":
            start = i
            seen_dot = c == "."
            seen_exp = False
            i += 1
            while i < n:
                ch = src[i]
                if ch.isdigit():
                    i += 1
                elif ch == "." and not seen_dot and not seen_exp:
                    seen_dot = True
                    i += 1
                elif ch in "eE" and not seen_exp:
                    seen_exp = True
                    i += 1
                    if i < n and src[i] in "+-":
                        i += 1
                else:
                    break
            literal = src[start:i]
            if literal in {".", "+", "-"} or literal.endswith(("e", "E", "e+", "e-", "E+", "E-")):
                raise LexError(f"Malformed number {literal!r} at position {start}")
            tokens.append(Token("NUM", literal, start))
            continue
        raise LexError(f"Unexpected character {c!r} at position {i}")
    return tokens


class _Parser:
    """Recursive-descent parser for the grammar:

        expr    := term   (('+'|'-') term)*
        term    := factor (('*'|'/'|'//'|'%') factor)*
        factor  := unary  ('**' factor)?          # right-associative
        unary   := ('+'|'-') unary | atom
        atom    := NUMBER | '(' expr ')'
    """

    def __init__(self, tokens: list[Token]):
        self._tokens = tokens
        self._it: Iterator[Token] = iter(tokens)
        self._peek: Token | None = next(self._it, None)

    def _advance(self) -> Token:
        tok = self._peek
        if tok is None:
            raise ParseError("Unexpected end of input")
        self._peek = next(self._it, None)
        return tok

    def _accept(self, kind: str, value: str | None = None) -> Token | None:
        tok = self._peek
        if tok is None or tok.kind != kind:
            return None
        if value is not None and tok.value != value:
            return None
        return self._advance()

    def parse(self) -> Number:
        result = self._expr()
        if self._peek is not None:
            raise ParseError(f"Unexpected token {self._peek.value!r} at position {self._peek.pos}")
        return result

    def _expr(self) -> Number:
        left = self._term()
        while self._peek and self._peek.kind == "OP" and self._peek.value in {"+", "-"}:
            op = self._advance().value
            right = self._term()
            left = left + right if op == "+" else left - right
        return left

    def _term(self) -> Number:
        left = self._factor()
        while self._peek and self._peek.kind == "OP" and self._peek.value in {"*", "/", "//", "%"}:
            op = self._advance().value
            right = self._factor()
            left = self._apply_binary(op, left, right)
        return left

    def _factor(self) -> Number:
        base = self._unary()
        if self._peek and self._peek.kind == "OP" and self._peek.value == "**":
            self._advance()
            exponent = self._factor()  # right-associative
            try:
                return base ** exponent
            except (OverflowError, ValueError) as exc:
                raise EvalError(f"Power error: {exc}") from exc
        return base

    def _unary(self) -> Number:
        if self._peek and self._peek.kind == "OP" and self._peek.value in {"+", "-"}:
            op = self._advance().value
            value = self._unary()
            return -value if op == "-" else +value
        return self._atom()

    def _atom(self) -> Number:
        tok = self._peek
        if tok is None:
            raise ParseError("Expected number or '('")
        if tok.kind == "NUM":
            self._advance()
            return _parse_number(tok.value)
        if tok.kind == "LP":
            self._advance()
            value = self._expr()
            if not self._accept("RP"):
                raise ParseError(f"Expected ')' at position {self._peek.pos if self._peek else len(self._tokens)}")
            return value
        raise ParseError(f"Unexpected token {tok.value!r} at position {tok.pos}")

    @staticmethod
    def _apply_binary(op: str, a: Number, b: Number) -> Number:
        try:
            if op == "*":
                return a * b
            if op == "/":
                return a / b
            if op == "//":
                return a // b
            if op == "%":
                return a % b
        except ZeroDivisionError as exc:
            raise EvalError("Division by zero") from exc
        raise ParseError(f"Unknown operator {op!r}")


def _parse_number(literal: str) -> Number:
    if any(ch in literal for ch in ".eE"):
        return float(literal)
    return int(literal)


def evaluate(expression: str) -> Number:
    """Parse and evaluate an arithmetic expression. Raises CalculatorError on failure."""
    tokens = tokenize(expression)
    if not tokens:
        raise ParseError("Empty expression")
    return _Parser(tokens).parse()


def repl() -> None:
    print("Calculator. Type an expression, 'help' for help, 'quit' to exit.")
    while True:
        try:
            line = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return
        cmd = line.strip()
        if not cmd:
            continue
        if cmd in {"quit", "exit"}:
            return
        if cmd == "help":
            print("Operators: + - * / // % **    Parentheses: ( )    Unary: + -")
            continue
        try:
            print(evaluate(cmd))
        except CalculatorError as exc:
            print(f"error: {exc}")


def main(argv: list[str] | None = None) -> int:
    import sys

    args = sys.argv[1:] if argv is None else argv
    if not args:
        repl()
        return 0
    expression = " ".join(args)
    try:
        print(evaluate(expression))
        return 0
    except CalculatorError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
