#!/usr/bin/env python3
"""main flask app  module"""
from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route("/")
def index():
    """index page"""
    return render_template("0-index.html")


if __name__ == "__main__":
    app.run(port="8080", debug=True)
