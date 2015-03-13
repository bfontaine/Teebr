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
* `TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_SECRET`,
  `TWITTER_ACCESS_TOKEN_KEY`, `TWITTER_ACCESS_TOKEN_SECRET`: Twitter API tokens


### Collect data

    make collect

It’ll populate the SQLite database. Press `^C` when you want to stop.
