# Teebr

A project for a Data Mining course. Live demo at [teebr.co](http://teebr.co).

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

    make seed-db

It’ll populate the SQLite database with a real-time status flow. Press `^C`
when you want to stop. Running it for less than five minutes is sufficient for
a demo.

Then, run `make collect` periodically. It’ll fetch the timeline of each DB
producer. This is more important than the previous step because we want to have
a lot of tweets per producer. The first step gives us a lot of tweets but also
a lot of producers.

### Run

Run the Web app with `make run`. Note that you’ll need to setup a local domain
to get the Twitter auth to work.

Open your `/etc/hosts` file and add the following line:

    127.0.0.1 dev.example.com

Now in your Twitter app settings, set the OAuth callback to:

    http://dev.example.com:8000/_oauth/twitter

You’ll need to access the app at `http://dev.example.com:8000` instead of
`http://localhost:8000`.

### TL;DR

1. Export the environment variables
2. Run `make run` and open your browser at `dev.example.com:8000` (see above
   for the setup)
3. Sign in the app with your Twitter account
4. Stop the app
5. Run `make seed-db` for a couple of minutes
6. Stop it
7. Run `make collect`
8. Stop it when you think you have enough tweets
9. Start the app again
