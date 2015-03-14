# -*- coding: UTF-8 -*-

from flask import Flask
from flask.ext.babel import Babel

from .oauth import authorize_oauth, twitter

# silent pyflakes
authorize_oauth, twitter

app = Flask("app")
app.config.from_pyfile('teebr.cfg')

# i18n
babel = Babel(app)


def get_languages(as_str=False):
    langs = babel.list_translations()
    if as_str:
        return map(str, langs)
    return langs
