var app = angular.module('tbTeebr',
  ['ui.bootstrap', 'tbUtils', 'mgo-mousetrap', 'ngAnimate']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('_{');
  $interpolateProvider.endSymbol('}_');
});


/*== Filters ================================================================*/

app.filter("tweet_html", ["$sce", function($sce) {

  var re_hashtag = /(^|\s)#([a-z][^.\s]*)/gi,
      // see:
      // https://github.com/twitter/twitter-text/blob/master/js/pkg/twitter-text-1.9.4.js#L343
      re_stock =  /(^|\s)\$([a-z]{1,6}(?:[._][a-z]{1,2})?)(\s|$)/gi,

      re_mention = /(^|\s)@([a-z]\w*)/gi,

      re_url = /(^|\s)(https?:\/\/)([a-z]+\.[a-z]{2,}\S+)/g;

  function highlightTwitterFeatures(text) {
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
      var full = protocol + url;

      return before + '<a rel="nofollow" target="_blank" ' +
        'class="status-link" href="' + full + '">' +
          '<span class="status-link-protocol">' + protocol + '</span>' +
            '<span class="status-link-url">' + url + '</span></a>';

    });
  }

  return function(text) {
    if (!text) { return text; }

    //text = text.replace(/</, '&lt;').replace(/>/, '&gt;');

    text = highlightTwitterFeatures(text);

    return $sce.trustAsHtml(text);
  };
}]);
