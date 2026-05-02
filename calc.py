def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}


def calculate(a, op, b):
    if op not in OPERATIONS:
        raise ValueError(f"Unknown operator: {op}")
    return OPERATIONS[op](a, b)


def main():
    print("Simple Calculator")
    print("Operations: +, -, *, /")
    try:
        a = float(input("First number: "))
        op = input("Operator: ").strip()
        b = float(input("Second number: "))
        print(f"Result: {calculate(a, op, b)}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
