#!/usr/bin/env python3
"""
6-app.py - Flask app with enhanced i18n locale selection.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, format_datetime, gettext as _
from typing import Optional, Dict
import pytz
from pytz.exceptions import UnknownTimeZoneError
from datetime import datetime


class Config:
    """Config class for Flask-Babel"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)

# Mocked user database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Optional[Dict]:
    """Get user from query string or return None"""
    try:
        user_id = int(request.args.get('login_as'))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """Set user on global before each request"""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Determine the best match language."""
    # 1. Locale from URL parameter
    locale = request.args.get("locale")
    if locale in app.config["LANGUAGES"]:
        g.locale = locale
        return locale

    # 2. Locale from user settings
    if g.get('user'):
        user_locale = g.user.get("locale")
        if user_locale in app.config["LANGUAGES"]:
            g.locale = user_locale
            return user_locale

    # 3. Locale from request headers
    selected = request.accept_languages.best_match(app.config["LANGUAGES"])
    g.locale = selected
    return selected


@babel.timezoneselector
def get_timezone():
    # Step 1: Check for timezone in URL query parameter
    tz_param = request.args.get("timezone")
    if tz_param:
        try:
            return pytz.timezone(tz_param).zone
        except UnknownTimeZoneError:
            pass

    # Step 2: Check if user is logged in and has a valid timezone
    user = getattr(g, "user", None)
    if user:
        user_tz = user.get("timezone")
        if user_tz:
            try:
                return pytz.timezone(user_tz).zone
            except UnknownTimeZoneError:
                pass

    # Step 3: Fallback default
    return "UTC"


@app.route('/')
def index():
    current_time = datetime.utcnow()
    tzname = g.get('timezone', 'UTC')
    try:
        tz = pytz.timezone(tzname)
        local_time = pytz.utc.localize(current_time).astimezone(tz)
    except Exception:
        local_time = current_time  # fallback

    formatted_time = format_datetime(local_time)
    return render_template('index.html', current_time=formatted_time)


if __name__ == "__main__":
    app.run()
