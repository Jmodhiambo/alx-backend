#!/usr/bin/env python3
"""Basic Flask app with Babel"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Config class for Flask-Babel"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Determine the best match language."""
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def index():
    """Home page"""
    return render_template('2-index.html')
