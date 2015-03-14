# -*- coding: UTF-8 -*-

from flask import session, request, redirect, url_for, flash
from flask.ext.babel import gettext
from flask_oauth import OAuth

from ..config import config

oauth = OAuth()

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=config["TWITTER_CONSUMER_KEY"],
    consumer_secret=config["TWITTER_CONSUMER_SECRET"],
)

@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')

def authorize_oauth(resp):
    """
    Call this from a route: ::

        @app.route('/oauth-authorized')
        @twitter.authorized_handler
        def oauth_authorized(resp):
            return authorize_oauth(resp)

    """
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(gettext(u'You denied the request to sign in.'))
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    return redirect(next_url)
