""" Migration template. """

import sys
# hacky way to be able to import teebr.models
sys.path.append("/Users/baptiste/Github/Teebr")

from peewee import *  # noqa
from teebr.models import IndicatorField


def migrate(migrator, database):
    """
    Write your migrations here.

    > migrator.create_table(model)
    > migrator.create_tables(model1, model2)
    > migrator.drop_table(model)
    > migrator.drop_tables(model1, model2)
    > migrator.add_column(table, name, field)
    > migrator.drop_column(table, name, field, cascade=True)
    > migrator.rename_column(table, old_name, new_name)
    > migrator.rename_table(old_name, new_name)
    > migrator.add_index(table, columns, unique=False)
    > migrator.drop_index(table, index_name)
    > migrator.add_not_null(table, column)
    > migrator.drop_not_null(table, column)

    XXX: not sure this works
    """
    with open("most_common_words.txt") as f:
        for word in [l.strip() for l in f]:
            word = word.lower()
            for table in ("consumer", "producer", "status"):
                field = IndicatorField("word:%s" % word)
                name = "sg_mc_word_%s" % word
                migrator.add_column(table, name, field)
                migrator.add_not_null(table, name)
