# -*- coding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals

# These are some functions used to maintain the DB/app, mainly to clean up the
# DB using the new code.

from sys import stdout

from .models import Status, Producer
from .text.spam import is_spam
from .text.utils import extract_named_entities

def remove_spam_statuses_from_db(delete=False, delete_author=False):
    """
    Remove the spammy statuses from the DB. With no arguments it only prints
    the number of statuses/producer it found. With `delete` set to `True` it'll
    delete spammy statuses, and with `delete_author` set to `True` it'll delete
    an account an all their statuses if one status is spammy.
    """
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


def recompute_entities_in_db(verbose=True):
    """
    Re-compute entities on all statuses in the DB. This is an expensive
    computation, only do that if you know what you're doing.
    """
    n = 0

    for st in Status.select():
        st.names = ",".join(extract_named_entities(st.text))
        st.save()
        if verbose:
            n = (n + 1) % 100
            if n == 0:
                stdout.write(".")
                stdout.flush()
