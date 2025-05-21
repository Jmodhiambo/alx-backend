#!/usr/bin/env python3
"""Basic Flask app with Babel"""

from flask import Flask, render_template, request
from flask_babel import Babel
from typing import Optional, List


class Config:
    """Config class for Flask-Babel"""
    LANGUAGES: List[str] = ["en", "fr"]
    BABEL_DEFAULT_LOCALE: str = "en"
    BABEL_DEFAULT_TIMEZONE: str = "UTC"


app: Flask = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel: Babel = Babel(app)


@babel.localeselector
def get_locale() -> Optional[str]:
    """Determine the best match language."""
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def index() -> str:
    """Home page"""
    return render_template('3-index.html')


if __name__ == "__main__":
    app.run()
