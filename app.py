# -*- coding: UTF-8 -*-

from json import dumps

from flask import render_template, g, request, url_for, redirect
from flask import session, Response, abort
from flask.ext.babel import gettext
from flask.ext.assets import Environment, Bundle
from webassets_iife import IIFE

from teebr.admin import setup_admin
from teebr.log import mkLogger
from teebr.models import status_to_dict
from teebr.pipeline import rate_status
from teebr.data_imports import import_credentials
from teebr.users import get_consumer_profile, get_unrated_statuses
from teebr.users import set_user_settings, mark_status_as_spam
from teebr.users import reset_user_ratings
from teebr.web import twitter, authorize_oauth, app, babel, get_languages

# admin
setup_admin(app)

# logs
logger = mkLogger('app')

# assets
assets = Environment(app)

js_filters = []
css_filters = []

if not app.config['DEBUG']:
    js_filters += [IIFE] #, 'closure_js']
    css_filters += ['cssmin']
    #assets.config["CLOSURE_EXTRA_ARGS"] = ['--language_in', 'ECMASCRIPT5']

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
    'js/app_home.js',
    'js/app_settings.js',
    'js/app_recommendations.js',
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

def user_header(s):
    g.header = s.format(g.user.screen_name)


@app.before_request
def set_current_user():
    username = session.get('twitter_user')
    if username and '/static/' not in request.path:
        setattr(g, 'user', get_consumer_profile(username))
    else:
        setattr(g, 'user', None)


@app.before_request
def set_header():
    setattr(g, 'header', gettext('Teebr'))


@app.before_request
def set_g_locale():
    if '/static/' not in request.path:
        logger.debug("setting user locale...")
        setattr(g, 'locale', babel.locale_selector_func())


@babel.localeselector
def get_locale():
    trs = get_languages(True)
    # 1. ?locale=
    locale_param = request.args.get('locale') or request.args.get('lang')
    if locale_param:
        if locale_param[:2] in trs:
            logger.debug("Known locale param: %s", locale_param)
            return locale_param
        logger.debug("Unknown locale param: %s", locale_param)
    # 2. user.locale
    if g.user and g.user.language[:2] in trs:
        logger.debug("Using user locale")
        return g.user.language
    # 3. request header
    logger.debug("locale: fall back in headers")
    return request.accept_languages.best_match(trs)


@app.route('/')
def index():
    if g.user:
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
    resp = authorize_oauth(resp)

    import_credentials(get_consumer_profile(session.get('twitter_user')),
            session.get('twitter_token'))

    return resp

@app.route('/home')
def home():
    if not g.user:
        return redirect(url_for("index"))

    user_header(gettext(u"@{}’s Home"))
    return render_template('home.html')


@app.route('/settings')
def user_settings():
    if not g.user:
        return redirect(url_for("index"))

    langs = babel.list_translations()
    lst = [{"code": l.language, "display": l.display_name} for l in langs]

    user_header(gettext(u"@{}’s Settings"))
    return render_template('settings.html', languages=lst)


@app.route('/recommendations')
def user_recommendations():
    if not g.user:
        return redirect(url_for("index"))

    return render_template('recommendations.html')

# AJAX routes

def json(what, code=200):
    return Response(dumps(what), code, mimetype='application/json')

def ajax(route, *args, **kw):
    return app.route("/_ajax%s" % route, *args, **kw)


@ajax("/user/statuses/unrated")
def unrated_statuses_sample():
    if not g.user:
        abort(404)

    return json(map(status_to_dict, get_unrated_statuses(g.user)))


@ajax("/user/statuses/rate", methods=["POST"])
def user_rate_status():  # ?score={0,1}&id=...
    if not g.user:
        logger.warn("Can't find rating user")
        abort(403)

    payload = request.get_json()
    if not payload:
        abort(400)

    score = payload['score']
    st_id = int(payload['id'])

    if score not in (0, 1):
        logger.debug("Invalid score: %s" % score)
        abort(400)

    if score == 0:
        score = -1

    rate_status(g.user, st_id, score)

    return json(None)


@ajax("/user/statuses/report", methods=["POST"])
def user_report_spam():  # ? id=...
    if not g.user:
        logger.warn("Can't find reporting user")
        abort(403)

    payload = request.get_json()
    if not payload:
        abort(400)

    st_id = int(payload['id'])

    mark_status_as_spam(st_id)

    return json(None)


@ajax("/user/reset-account", methods=["POST"])
def user_reset_account():
    if not g.user:
        logger.warn("Can't find reset an unknown user")
        abort(403)

    reset_user_ratings(g.user)

    return json(None)


@ajax("/user/settings", methods=["POST"])
def user_change_settings():
    if not g.user:
        logger.warn("Can't change settings of an unknown user")
        abort(403)

    payload = request.get_json()
    if not payload:
        abort(400)

    changed = set_user_settings(g.user, payload["settings"])

    return json({"reload": changed})
