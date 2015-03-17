# -*- coding: UTF-8 -*-

# ref: https://github.com/mrjoes/flask-admin/blob/master/examples/peewee/app.py

from __future__ import absolute_import, unicode_literals

from flask.ext import admin
from flask.ext.admin.contrib.peewee import ModelView

from .models import Producer, Consumer, Status

# Note: no authentication is provided here

class ModelAdminView(ModelView):
    # read only
    can_create = False
    can_edit = False
    can_delete = False

    page_size = 50

class ProducerAdmin(ModelAdminView):
    pass

class ConsumerAdmin(ModelAdminView):
    pass

class StatusAdmin(ModelAdminView):
    pass

def setup_admin(app):
    app_admin = admin.Admin(app, name=u"Teebr Admin")
    app_admin.add_view(ProducerAdmin(Producer))
    app_admin.add_view(ConsumerAdmin(Consumer))
    app_admin.add_view(StatusAdmin(Status))
    return app_admin
