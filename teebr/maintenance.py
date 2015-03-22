# -*- coding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals

from .models import Status, Producer
from .text.spam import is_spam

def remove_spam_statuses_from_db(delete=False, delete_author=False):
    all_statuses = 0
    spam_statuses = 0

    spam_authors = set()

    for st in Status.select():
        all_statuses += 1
        if is_spam(st.text):
            try:
                author = st.author
            except Producer.DoesNotExist:
                # This happen when we deleted all tweets from an author before
                # this one, which has thus been deleted
                continue

            # stats
            if author.screen_name not in spam_authors:
                spam_authors.add(author.screen_name)
                spam_statuses += len(list(author.statuses))

            if delete_author:
                # delete the author and all its statuses. This one is pretty
                # aggressive and will very likely delete some false positives.
                author.delete_instance(recursive=True)
            elif delete:
                # delete only the status. This one is light and we'll keep spam
                # accounts in the DB
                st.delete_instance()

    print "All statuses:  %5d" % all_statuses
    print "Spam statuses: %5d" % spam_statuses
    print "Spam authors:  %5d" % len(spam_authors)
