# Teebr

A project for a Data Mining course.

## Build

### Docs

You need LaTeX, with `csquotes`. If you have TexLive, install it with its
package manager:

    $ tlmgr install csquotes

### Environment

You’ll need to set the following environment variables:

* `TEEBR_SQLITE_DB_PATH`: A path to a local SQLite database file. It’ll be
  created if it doesn’t exist.
* `NLTK_DATA`: A path to your NLTK data directory.
* `TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_SECRET`: Twitter API tokens

The stream importer uses the first credentials it finds in the database, so you
need to have at least one user signed in with Twitter before starting it.

### Collect data

    make collect

It’ll populate the SQLite database. Press `^C` when you want to stop.
