var app = angular.module('tbTeebr',
  ['ui.bootstrap', 'tbUtils', 'mgo-mousetrap', 'ngAnimate']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('_{');
  $interpolateProvider.endSymbol('}_');
});


/*== Filters ================================================================*/

app.filter("tweet_html_text", ["$sce", function($sce) {

  var re_hashtag = /(^|\s)#([a-z][^.\s]*)/gi,
      // see:
      // https://github.com/twitter/twitter-text/blob/master/js/pkg/twitter-text-1.9.4.js#L343
      re_stock =  /(^|\s)\$([a-z]{1,6}(?:[._][a-z]{1,2})?)(\s|$)/gi,

      re_mention = /(^|\s)@([a-z]\w*)/gi,

      re_url = /(^|\s)(https?:\/\/)([a-z0-9]+\.[a-z0-9]{2,}\S+)/g;

  function highlightTwitterFeatures(text, entities) {
    return text.replace(re_hashtag, function(_, before, tag) {

      return before + '<span class="status-hashtag">' +
        '<span class="status-hash">#</span>' +
          '<span class="status-hashtag-content">' + tag + '</span></span>';

    }).replace(re_stock, function(_, before, tag, after) {

      return before + '<span class="status-cashtag">' +
        '<span class="status-cash">$</span>' +
          '<span class="status-cashtag-content">' + tag + '</span></span>' +
            after;

    }).replace(re_mention, function(_, before, mention) {

      return before + '<span class="status-mention">' +
        '<span class="status-at">@</span>' +
          '<span class="status-mention-content">' + mention + '</span></span>';

    }).replace(re_url, function(_, before, protocol, url) {
      var full = protocol + url,
          max_length = 30,

          photos = entities.photos || [];

      for (var i=0, l=photos.length; i<l; i++) {
        if (photos[i].url == full) {

          // if this is a picture URL, remove it entirely because we'll show
          // the photo below the text
          return before;
        }
      }

      if (url.length > max_length) {
        url = url.slice(0, max_length-1) + "…";
      }

      return before + '<a rel="nofollow" target="_blank" ' +
        'class="status-link" href="' + full + '">' +
          '<span class="status-link-protocol">' + protocol + '</span>' +
            '<span class="status-link-url">' + url + '</span></a>';

    });
  }

  return function(s) {
    var text;

    if (!s) { return s; }

    text = s.text;

    if (!text) { return text; }

    //text = text.replace(/</, '&lt;').replace(/>/, '&gt;');

    text = highlightTwitterFeatures(text, s.extra_entities || {});

    return $sce.trustAsHtml(text);
  };
}]);
