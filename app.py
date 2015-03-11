# -*- coding: UTF-8 -*-

from json import dumps

from flask import Flask, render_template, g, request, url_for, redirect
from flask import session, Response, abort
from flask.ext.assets import Environment, Bundle
from flask.ext.babel import Babel
from webassets_iife import IIFE

from teebr.admin import setup_admin
from teebr.log import mkLogger
from teebr.models import status_to_dict
from teebr.pipeline import get_consumer_profile, get_unrated_statuses
from teebr.web import twitter, authorize_oauth

app = Flask(__name__)
app.config.from_pyfile('teebr.cfg', silent=True)

# admin
setup_admin(app)

# logs
logger = mkLogger('app')

# i18n
babel = Babel(app)

# assets
assets = Environment(app)

js_filters = []
css_filters = []

if not app.config['DEBUG']:
    js_filters += [IIFE] #, 'closure_js']
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
    username = session.get('twitter_user')
    if username and '/static/' not in request.path:
        setattr(g, 'user', get_consumer_profile(username))


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
    # 2. request header
    logger.debug("locale: fall back in headers")
    return request.accept_languages.best_match(trs)


@app.route('/')
def index():
    if session.get("twitter_user"):
        return redirect(url_for("home"))

    return render_template('main.html')

@app.route('/_login/twitter')
def twitter_login():
    next_url = request.args.get('next') or request.referrer or url_for("home")
    return twitter.authorize(callback=url_for('oauth_authorized', next=next_url))


@app.route('/_logout/twitter')
def twitter_logout():
    session.clear()
    return redirect(url_for("index"))


@app.route('/_oauth/twitter')
@twitter.authorized_handler
def oauth_authorized(resp):
    return authorize_oauth(resp)

@app.route('/home')
def home():
    if not session.get("twitter_user"):
        return redirect(url_for("home"))

    return render_template('home.html')


# AJAX routes

def json(what, code=200):
    return Response(dumps(what), code, mimetype='application/json')

def ajax(route):
    return app.route("/_ajax%s" % route)

@ajax("/user/statuses/unrated")
def unrated_statuses_sample():
    user = get_consumer_profile(session.get("twitter_user"))
    if not user:
        abort(404)

    return json(map(status_to_dict, get_unrated_statuses(user)))
