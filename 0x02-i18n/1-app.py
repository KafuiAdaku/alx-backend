#!/usr/bin/env python3
"""main flask app  module"""
from flask import Flask
from flask import render_template
from flask_babel import Babel


class Config:
    """Configuration class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.route("/")
def index():
    """index page"""
    return render_template("1-index.html")


if __name__ == "__main__":
    app.run(port="8080", debug=True)
