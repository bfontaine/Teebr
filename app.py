# -*- coding: UTF-8 -*-

from flask import Flask, render_template, g, request, session
from flask.ext.assets import Environment, Bundle
from flask.ext.babel import Babel
from webassets_iife import IIFE

from teebr import store
from teebr.flaskutils import unlogged_only, user
from remindme.log import mkLogger

app = Flask(__name__)
app.config.from_pyfile('teebr.cfg', silent=True)

logger = mkLogger('app')

# i18n
babel = Babel(app)

# assets
assets = Environment(app)

js_filters = []
css_filters = []

if not app.config['DEBUG']:
    js_filters += [IIFE, 'closure_js']
    css_filters += ['cssmin']
    assets.config["CLOSURE_EXTRA_ARGS"] = ['--language_in', 'ECMASCRIPT5']

# - JS
js = Bundle(
    # Bootstrap/Bootflat
    'js/vendor/jquery.js',
    'js/vendor/html5shiv.js',
    # 'js/vendor/icheck.min.js',
    'js/vendor/bootstrap.min.js',
    'js/vendor/angular.js',
    'js/vendor/angular-animate.js',
    'js/vendor/mousetrap.js',
    'js/vendor/wMousetrap.js',
    'js/vendor/ui-bootstrap-tpls-0.11.0.js',
    # Our JS
    'js/utils.js',
    'js/app.js',
    filters=js_filters,
    output='js/teebr.js')
assets.register('js_all', js)

# - CSS
css = Bundle(
    # Bootstrap/Bootflat
    'css/bootstrap.min.css',
    'css/bootflat.min.css',
    # Our JS
    'css/app.css',
    filters=css_filters,
    output='css/teebr.css')
assets.register('css_all', css)


@app.before_request
def set_current_user():
    _id = session.get('_id')
    if _id and '/static/' not in request.path:
        setattr(g, 'user', store.get_user(_id=_id))


@app.before_request
def set_g_locale():
    if '/static/' not in request.path:
        logger.debug("setting user locale...")
        setattr(g, 'locale', babel.locale_selector_func())


@babel.localeselector
def get_locale():
    trs = [str(t) for t in babel.list_translations()]
    # 1. ?locale=
    locale_param = request.args.get('locale') or request.args.get('lang')
    if locale_param:
        if locale_param[:2] in trs:
            logger.debug("Known locale param: %s", locale_param)
            return locale_param
        logger.debug("Unknown locale param: %s", locale_param)
    # 2. user.locale
    u = user()
    if u and u.locale:
        logger.debug("Using user locale")
        return u.locale
    # 3. request header
    logger.debug("locale: fall back in headers")
    return request.accept_languages.best_match(trs)


@app.route('/')
@unlogged_only
def index():
    return render_template('main.html')
