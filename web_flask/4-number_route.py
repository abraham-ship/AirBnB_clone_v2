#!/usr/bin/python3

'''
script that starts a Flask web application:
    /: display “Hello HBNB!”
    /hbnb: display “HBNB”
    /c/<text>: display “C ”, followed by the value of the text variable
    /python/(<text>): display “Python ”, followed by the value of the text
        The default value of text is “is cool”
    /number/<n>: display “n is a number” only if n is an integer
'''
from flask import Flask, abort


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def show_hbnb():
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def show_c(text):
    text = text.replace('_', ' ')
    return "C " + text


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>")
def pythoniscool(text='is cool'):
    text = text.replace('_', ' ')
    return "Python " + text


@app.route("/number/<n>", strict_slashes=False)
def show_number(n):
    if n.isdigit():
        return n + " is a number"
    else:
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
