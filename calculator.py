import math
import re


class CalcError(Exception):
    pass


_NUMBER_RE = re.compile(r"\d+(?:\.\d*)?(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?")


def tokenize(s):
    tokens = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
            continue
        if c in "+-*/()":
            tokens.append((c, c))
            i += 1
            continue
        m = _NUMBER_RE.match(s, i)
        if m:
            tokens.append(("NUM", float(m.group())))
            i = m.end()
            continue
        raise CalcError(f"unexpected character {c!r} at position {i}")
    tokens.append(("END", None))
    return tokens


class _Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse(self):
        node = self.expr()
        if self.peek()[0] != "END":
            raise CalcError(f"unexpected token {self.peek()[1]!r}")
        return node

    def expr(self):
        node = self.term()
        while self.peek()[0] in ("+", "-"):
            op = self.advance()[0]
            right = self.term()
            node = ("binop", op, node, right)
        return node

    def term(self):
        node = self.factor()
        while self.peek()[0] in ("*", "/"):
            op = self.advance()[0]
            right = self.factor()
            node = ("binop", op, node, right)
        return node

    def factor(self):
        tok = self.peek()
        if tok[0] in ("+", "-"):
            op = self.advance()[0]
            return ("unary", op, self.factor())
        if tok[0] == "NUM":
            self.advance()
            return ("num", tok[1])
        if tok[0] == "(":
            self.advance()
            node = self.expr()
            if self.peek()[0] != ")":
                raise CalcError("unbalanced parens")
            self.advance()
            return node
        if tok[0] == "END":
            raise CalcError("unexpected end of expression")
        raise CalcError(f"unexpected token {tok[1]!r}")


def _eval(node):
    kind = node[0]
    if kind == "num":
        return node[1]
    if kind == "unary":
        v = _eval(node[2])
        return v if node[1] == "+" else -v
    if kind == "binop":
        op, l, r = node[1], _eval(node[2]), _eval(node[3])
        if op == "+":
            return l + r
        if op == "-":
            return l - r
        if op == "*":
            return l * r
        if op == "/":
            if r == 0:
                raise CalcError("division by zero")
            return l / r
    raise CalcError("internal error")


def evaluate(expression):
    if not expression or not expression.strip():
        raise CalcError("empty expression")
    tokens = tokenize(expression)
    tree = _Parser(tokens).parse()
    return _eval(tree)


def format_result(value):
    if math.isfinite(value) and value == int(value) and abs(value) < 1e16:
        return str(int(value))
    return repr(value)
