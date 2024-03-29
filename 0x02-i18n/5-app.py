#!/usr/bin/env python3
"""main flask app  module - forced local with url parameter"""
from flask import Flask, request, g
from flask import render_template
from flask_babel import Babel, _


class Config:
    """Configuration class
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale():
    """Gets local language
        Returns:
            _type_: _description_
    """
    locale = request.args.get('locale')
    if locale and locale in app.config["LANGUAGES"]:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """
    User login mock.
    Gets a user from a dictionary

    returns:
        int: user id
    """
    user_id = request.args.get("login_as")
    if user_id and int(user_id) in users:
        return users[int(user_id)]
    return None


@app.before_request
def before_request():
    """
    Stores the requested user in the global varialble g
    """
    user = get_user()
    g.user = user


@app.route("/")
def index():
    """index page route
        Returns:
            _summary_
    """
    return render_template("5-index.html")


if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0", debug=True)
