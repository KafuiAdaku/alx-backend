#!/usr/bin/env python3
"""main flask app  module"""
from flask import Flask, request
from flask import render_template
from flask_babel import Babel, _


class Config:
    """Configuration class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Gets local language"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route("/")
def index():
    """index page route"""
    return render_template("3-index.html")


if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0", debug=True)
