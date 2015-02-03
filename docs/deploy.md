# Deploy Teebr

## On Dokku

`ENV` should contain:

    export ELASTICSEARCH_URL='http://...:9200'
    export TWITTER_CONSUMER_KEY='...'
    export TWITTER_CONSUMER_SECRET='...'

`CHECK` can contain checks to see if the application is online.
[See here][checks].

[checks]: https://github.com/broadly/dokku/blob/master/plugins/checks/check-deploy
