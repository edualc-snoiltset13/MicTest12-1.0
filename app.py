from collections import deque

from flask import Flask, render_template, request

from calculator import CalcError, evaluate, format_result

app = Flask(__name__)
history = deque(maxlen=10)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    expression = ""
    if request.method == "POST":
        expression = request.form.get("expression", "").strip()
        try:
            result = format_result(evaluate(expression))
        except CalcError as e:
            result = f"Error: {e}"
        if expression:
            history.appendleft((expression, result))
    return render_template(
        "index.html",
        expression=expression,
        result=result,
        history=list(history),
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
