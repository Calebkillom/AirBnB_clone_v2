#!/usr/bin/python3
"""A script that starts a Flask web application."""

from flask import Flask, render_template
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """function that displays Hello HBNB."""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def dis_hbnb():
    """function that displays HBNB."""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
@app.route("/c/", strict_slashes=False)
def display_c(text="is cool"):
    """function that displays C followed by value of text variable."""
    text = text.replace('_', ' ')
    return "C {}".format(text)


@app.route("/python/<text>", strict_slashes=False)
@app.route("/python", strict_slashes=False)
def display_python(text="is cool"):
    """function that displays python followed by value of text variable."""
    text = text.replace('_', ' ')
    return "Python {}".format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    """Function that display “n is a number” only if n is an integer."""
    if isinstance(n, int):
        return "{} is a number".format(n)

@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """function that displays a HTML page only if n is an integer."""
    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
