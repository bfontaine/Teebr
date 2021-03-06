""" Migration template. """

from peewee import *  # noqa

# class Consumer(User):
#   + beta_features = BooleanField(default=False)
#   + is_admin = BooleanField(default=False)

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

    """
    migrator.add_column("consumer", "beta_features", BooleanField(default=False))
    migrator.add_column("consumer", "is_admin", BooleanField(default=False))
