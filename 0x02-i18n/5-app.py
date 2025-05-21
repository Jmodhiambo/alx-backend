#!/usr/bin/env python3
"""Basic Flask app with Babel"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Optional, Dict, Any, List


class Config:
    """Config class for Flask-Babel"""
    LANGUAGES: List[str] = ["en", "fr"]
    BABEL_DEFAULT_LOCALE: str = "en"
    BABEL_DEFAULT_TIMEZONE: str = "UTC"


app: Flask = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel: Babel = Babel(app)

# Mocked user database
users: Dict[int, Dict[str, Optional[str]]] = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Optional[Dict[str, Optional[str]]]:
    """Get user from query string or return None"""
    try:
        user_id: Optional[str] = request.args.get('login_as')
        if user_id is not None:
            return users.get(int(user_id))
    except (TypeError, ValueError):
        return None
    return None


@app.before_request
def before_request() -> None:
    """Set user on global before each request"""
    g.user = get_user()


@babel.localeselector
def get_locale() -> Optional[str]:
    """Determine the best match language."""
    # Check if locale is passed via URL parameter and is supported
    locale: Optional[str] = request.args.get("locale")
    if locale in app.config["LANGUAGES"]:
        g.locale = locale
        return locale

    # Locale from logged in user
    if g.get('user'):
        user_locale: Optional[str] = g.user.get("locale")
        if user_locale in app.config["LANGUAGES"]:
            g.locale = user_locale
            return user_locale

    # Fallback to Accept-Language header
    selected: Optional[str] = request.accept_languages.best_match(
        app.config["LANGUAGES"]
    )
    g.locale = selected
    return selected


@app.route('/')
def index() -> str:
    """Home page"""
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run()
