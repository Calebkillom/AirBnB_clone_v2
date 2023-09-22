#!/usr/bin/python3
# script that starts a Flask web application


from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """function that returns Hello HBNB!."""
    return "Hello HBNB!"


if __name__ == "__main__":
    """application listening on 0.0.0.0, port 5000."""
    app.run(host='0.0.0.0', port=5000)
