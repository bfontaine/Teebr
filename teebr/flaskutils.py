# -*- coding: UTF-8 -*-

from flask.ext.babel import gettext
from flask import g, redirect, url_for, session


def user():
    """
    Return the currently connected user
    """
    return getattr(g, 'user', None)


###############################################################################
# Redirections
###############################################################################

def _redirect_cond(cond, url_str, name):
    def _deco(fun):
        def _fun(*args, **kwargs):
            if cond():
                return redirect(url_for(url_str))
            return fun(*args, **kwargs)
        _fun.__name__ = fun.__name__
        return _fun
    _deco.__name__ = name
    return _deco

# decorator: redirect to /login if user is not logged in
logged_only = _redirect_cond(lambda: user() is None, 'login', 'logged_only')

# decorator: redirect to / if user is logged in
unlogged_only = _redirect_cond(lambda: user(), 'home', 'unlogged_only')


def redirect_for(s, code=302):
    """
    Shortcut for ``redirect(url_for(s), code)``.
    """
    return redirect(url_for(s), code)


###############################################################################
# Templates
###############################################################################

def setvar(name, value):
    """
    decorator to set a variable on 'g'
    """
    def _deco(fun):
        def _fun(*args, **kwargs):
            _value = gettext(value) if isinstance(value, str) else value
            setattr(g, name, _value)
            return fun(*args, **kwargs)

        _fun.__name__ = fun.__name__
        return _fun

    return _deco


# shortcut
title = lambda v: setvar('title', v)
